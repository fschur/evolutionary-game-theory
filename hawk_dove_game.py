import numpy as np
import matplotlib.pyplot as plt
import random
import itertools

lookup = {"[0, 1]": "hawk", "[1, 0]": "dove"}

#ToDo: conditional

#win={"dove": [1, 0.5, 2], "hawk": [0, 1.5, 2]}
#win={"dove": [1, 0, 2], "hawk": [0.6, 2, 2]}

class Game:
    def __init__(self, num_res=20000, win={"dove": [1, 0.5, 2], "hawk": [0.6, 1.5, 2]},
                 population=[[1, 0]]*39990 + [[0, 1]]*10, rep_val=0.1):

        population.sort()
        options = list(k for k, _ in itertools.groupby(population))
        print("List of types of individuals: ", options)

        """
        num_res: number of foodsources

        win: describes the game-table as a python dictionary: First entry is the reward when playing against the same
        kind of individual (dove, dove; hawk,hawk), second is the reward if playing against the opposing kind of
        individual, last entry is the reward for arriving at a food-resource alone.

        population: starting population. (in this case: hawks, mixed strategy with 30% dove and 70% hawk, dove)

        rep_val: reward needed for reproduction. I.e.  having reward of 1 keeps me alive (0.5) and allows me the
        reproduce once (additional 0.5).

        options: all possible type of individuals
        """
        self.num_res = num_res
        self.options = options
        self.rep_val = rep_val
        self.win = win
        self.population = population #current population
        self.log = {}
        # create log for all possible individuals
        for o in options:
            self.log[str(o)] = [population.count(o)]

        self.log_actual = {}
        # create log for all possible individuals
        for o in options:
            self.log_actual[str(o)] = []

        self.log_fit = {}
        # create log for all possible individuals
        for o in options:
            self.log_fit[str(o)] = []

        self.log_fit_overall = []

    def step(self):
        # distributes the individuals to the food sources, foodsource i is occupied by the ith and the (i + num_res)
        # entry in the array matchthing (if one slot is not occupied then this slot is indicated by [0, 0])
        indi = self.population
        # make it truly random
        random.shuffle(indi)
        idx = np.random.choice([s for s in range(2*self.num_res)], min(len(indi), 2*self.num_res), replace=False)
        # start with all empty slots
        matchings = [[0, 0]]*(2*self.num_res)
        # distribute the individuals on the foodsources
        for i, id in enumerate(idx):
            matchings[id] = indi[i]

        for o in self.options:
            self.log_actual[str(o)].append(matchings.count(o))

        self.log_fit_overall.append(0)

        new_pop = []
        for o in self.options:
            self.log_fit[str(o)].append(0)

        for i in range(self.num_res):
            # compute the rewards for each matching
            rewards = self.compute_rewards(matchings[i], matchings[i + self.num_res])
            # compute the amount of offspring
            self.log_fit_overall[-1] += sum(rewards)
            if matchings[i] != [0, 0]:
                self.log_fit[str(matchings[i])][-1] += rewards[0]
                for _ in range(int(rewards[0]/self.rep_val)):
                    new_pop.append(matchings[i])
            if matchings[i + self.num_res] != [0, 0]:
                for _ in range(int(rewards[1]/self.rep_val)):
                    new_pop.append(matchings[i + self.num_res])
                self.log_fit[str(matchings[i + self.num_res])][-1] += rewards[1]

        #update population
        self.population = new_pop
        # keep logs of current population
        for o in self.options:
            self.log[str(o)].append(self.population.count(o))

        self.log_fit_overall[-1] /= sum(np.array(list(self.log_actual.values()))[:, -1])

        for o in self.options:
            if self.log[str(o)][-2] != 0:
                self.log_fit[str(o)][-1] /= self.log_actual[str(o)][-1]
            else:
                self.log_fit[str(o)][-1] = 0

    def compute_rewards(self, first, second):
        first, second = self.decide(first, second)

        if first == second:
            if first == "d":
                reward = [self.win["dove"][0], self.win["dove"][0]]
            elif first == "h":
                reward = [self.win["hawk"][0], self.win["hawk"][0]]
            else:
                reward = [0, 0]
        else:
            if first == "d":
                if second == "h":
                    reward = [self.win["dove"][1], self.win["hawk"][1]]

                else:
                    reward = [self.win["dove"][2], 0]
            elif first == "h":
                if second == "d":
                    reward = [self.win["hawk"][1], self.win["dove"][1]]
                else:
                    reward = [self.win["hawk"][2], 0]
            elif first == "e":
                if second == "h":
                    reward = [0, self.win["hawk"][2]]
                elif second == "d":
                    reward = [0, self.win["dove"][2]]

        return reward

    def decide_cond(self, first, second):
        return

    def decide(self, first, second):
        # in the case of mixed strategy decide if the individuals act like a hawk or like a dove.
        if first == [0, 0]:
            first = "e"
        else:
            first = np.random.choice(["d", "h"], p=(first[0], first[1]))

        if second == [0, 0]:
            second = "e"
        else:
            second = np.random.choice(["d", "h"], p=(second[0], second[1]))

        return first, second

    def plot_data(self, save):
        # plots the logs as a stackedplot
        x = [i for i in range(len(self.log[str(self.options[0])]))]
        y = [self.log_actual[str(o)] for o in self.options]
        y_abs = [self.log[str(o)] for o in self.options]
        y_prob = np.array(y)*(1/np.sum(y, 0))
        y_total = np.sum(y_abs, 0)
        fitness = [self.log_fit[str(o)] for o in self.options]

        if self.options == [[1, 0], [0, 1]] or self.options == [[0, 1], [1, 0]]:
            options = [lookup[str(o)] for o in self.options]
        else:
            options = self.options

        print("Final distribution: " , np.array(y)[:, -1]/np.sum(np.array(y)[:, -1]))

        fig, ax = plt.subplots()
        ax.plot(x, y_total)
        ax.set(xlabel="timestep (t)", ylabel="population size", title="total population")
        plt.show()
        if save:
            fig.savefig("total_pop_num_res_" + str(self.num_res) + "_win_" + str(self.win).replace(".", "") + "_rep_val_" +
                        str(self.rep_val).replace(".", "") + "_options_" + str(self.options).replace(" ", ""))

        fig, ax = plt.subplots()
        for i, s in enumerate(y):
            ax.plot(x[1:], s, label=options[i])
        ax.set(xlabel="timestep (t)", ylabel="population size", title="population by type")
        ax.legend()
        plt.show()

        if save:
            fig.savefig("pop_type_size_num_res_" + str(self.num_res) + "_win_" + str(self.win).replace(".", "") + "_rep_val_" +
                        str(self.rep_val).replace(".", "") + "_options_" + str(self.options).replace(" ", ""))

        fig, ax = plt.subplots()
        for i, s in enumerate(list(y_prob)):
            ax.plot(x[1:], s, label=options[i])
        ax.set(xlabel="timestep (t)", ylabel="percent of total population", title="relative size")
        ax.legend()
        plt.show()
        if save:
            fig.savefig("perc_pop_type_num_res_" + str(self.num_res) + "_win_" + str(self.win).replace(".", "") + "_rep_val_" +
                        str(self.rep_val).replace(".", "") + "_options_" + str(self.options).replace(" ", ""))

        fig, ax = plt.subplots()
        for i, s in enumerate(fitness):
            ax.plot(x[1:], s, label=options[i])
        ax.plot(x[1:], self.log_fit_overall, label="overall")
        ax.set(xlabel="timestep (t)", ylabel="fitness", title="fitness by type")
        ax.legend()
        plt.show()
        if save:
            fig.savefig("fitness_num_res_" + str(self.num_res) + "_win_" + str(self.win).replace(".", "") + "_rep_val_" +
                        str(self.rep_val).replace(".", "") + "_options_" + str(self.options).replace(" ", ""))

        #plt.stackplot(x, y_abs)
        #plt.show()

"""
game = Game()

# run for 15 timesteps
for i in range(35):
    game.step()
game.plot_data()
"""