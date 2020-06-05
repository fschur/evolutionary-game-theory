import numpy as np
import matplotlib.pyplot as plt
import random
import itertools


class Game:
    def __init__(self, lookup={"[2]": "hawk", "[1]": "dove"}, colors={"dove": "blue", "hawk": "red"}, num_res=20000,
                 win=[np.array([[0, 0, 0], [2, 1, 0.5], [2, 1.5, 0.4]]), np.array([[2, 2, 2], [2, 1, 1.5], [2, 0.5, 0.4]])],
                 population=[[1]]*int(0.7*40000) + [[2]]*int(0.3*40000), rep_val=0.5):

        population.sort()
        options = list(k for k, _ in itertools.groupby(population))
        print("List of types of individuals: ", options)

        self.colors = colors
        self.lookup = lookup
        self.num_res = num_res
        self.options = options
        self.rep_val = rep_val
        self.win = win
        self.population = population #current population
        self.log = {}
        for o in options:
            self.log[str(o)] = [population.count(o)]

        self.log_actual = {}
        for o in options:
            self.log_actual[str(o)] = []

        self.log_fit = {}
        for o in options:
            self.log_fit[str(o)] = []

        self.log_fit_overall = []

    def step(self):
        indi = self.population
        random.shuffle(indi)
        idx = np.random.choice([s for s in range(2*self.num_res)], min(len(indi), 2*self.num_res), replace=False)
        matchings = [[0]]*(2*self.num_res)
        for i, id in enumerate(idx):
            matchings[id] = indi[i]

        for o in self.options:
            self.log_actual[str(o)].append(matchings.count(o))

        self.log_fit_overall.append(0)

        new_pop = []
        for o in self.options:
            self.log_fit[str(o)].append(0)

        for i in range(self.num_res):
            rewards = self.compute_rewards(matchings[i], matchings[i + self.num_res])
            self.log_fit_overall[-1] += sum(rewards)
            if matchings[i] != [0]:
                self.log_fit[str(matchings[i])][-1] += rewards[0]
                mean_offs = rewards[0]/self.rep_val
                z = int(mean_offs)
                diff = mean_offs - z
                offspring = np.random.choice([z, z+1], p=(1 - diff, diff))
                for _ in range(offspring):
                    new_pop.append(matchings[i])
            if matchings[i + self.num_res] != [0]:
                mean_offs = rewards[1]/self.rep_val
                z = int(mean_offs)
                diff = mean_offs - z
                offspring = np.random.choice([z, z+1], p=(1 - diff, diff))
                for _ in range(offspring):
                    new_pop.append(matchings[i + self.num_res])
                self.log_fit[str(matchings[i + self.num_res])][-1] += rewards[1]

        self.population = new_pop
        for o in self.options:
            self.log[str(o)].append(self.population.count(o))

        self.log_fit_overall[-1] /= sum(np.array(list(self.log_actual.values()))[:, -1])

        for o in self.options:
            if self.log_actual[str(o)][-1] != 0:
                self.log_fit[str(o)][-1] /= self.log_actual[str(o)][-1]
            else:
                self.log_fit[str(o)][-1] = 0

    def compute_rewards(self, first, second):
        first, second = self.decide(first, second)

        rewards = [0, 0]

        rewards[0] = self.win[0][first[0], second[0]]
        rewards[1] = self.win[1][first[0], second[0]]

        return rewards

    def decide(self, first, second):

        if len(first) != 1:
            first = [np.random.choice([1, 2], p=(first[0], first[1]))]

        if len(second) != 1:
            second = [np.random.choice([1, 2], p=(second[0], second[1]))]

        return first, second

    def plot_data(self, save):
        x = [i for i in range(len(self.log[str(self.options[0])]))]
        y = [self.log_actual[str(o)] for o in self.options]
        y_abs = [self.log[str(o)] for o in self.options]
        y_prob = np.array(y)*(1/np.sum(y, 0))
        y_total = np.sum(y_abs, 0)
        fitness = [self.log_fit[str(o)] for o in self.options]
        keys = list(self.lookup.keys())
        try:
            options = [self.lookup[str(o)] for o in self.options]
        except KeyError:
            options = self.options

        print("Final distribution: ", np.array(y)[:, -1]/np.sum(np.array(y)[:, -1]))

        fig, ax = plt.subplots()
        ax.plot(x, y_total)
        ax.set(xlabel="timestep (t)", ylabel="population size", title="total population")
        plt.ylim((0, 40000))
        plt.show()
        if save:
            fig.savefig("total_pop_num_res_")# + str(self.num_res) + "_win_" + str(self.win).replace(".", "") + "_rep_val_" + str(self.rep_val).replace(".", "") + "_options_" + str(self.options).replace(" ", "").replace(".", ""))

        fig, ax = plt.subplots()
        for i, s in enumerate(y):
            try:
                j = self.colors[str(options[i])]
                ax.plot(x[1:], s, color=j, label=options[i])
            except KeyError:
                ax.plot(x[1:], s, label=options[i])
        ax.set(xlabel="timestep (t)", ylabel="population size", title="population by type")
        ax.legend()
        plt.show()

        if save:
            fig.savefig("pop_type_size_num_res_")# + str(self.num_res) + "_win_" + str(self.win).replace(".", "") + "_rep_val_" +str(self.rep_val).replace(".", "") + "_options_" + str(self.options).replace(" ", "").replace(".", ""))

        fig, ax = plt.subplots()
        for i, s in enumerate(list(y_prob)):
            try:
                j = self.colors[str(options[i])]
                ax.plot(x[1:], s, color=j, label=options[i])
            except KeyError:
                ax.plot(x[1:], s, label=options[i])
        ax.set(xlabel="timestep (t)", ylabel="percent of total population", title="relative size")
        ax.legend()
        plt.ylim((0, 1))
        plt.show()
        if save:
            fig.savefig("perc_pop_type_num_res_") # + str(self.num_res) + "_win_" + str(self.win).replace(".", "") + "_rep_val_" + str(self.rep_val).replace(".", "") + "_options_" + str(self.options).replace(" ", "").replace(".", ""))

        fig, ax = plt.subplots()
        for i, s in enumerate(fitness):
            try:
                j = self.colors[str(options[i])]
                ax.plot(x[1:], s, j, label=options[i])

            except KeyError:
                ax.plot(x[1:], s, label=options[i])

        if len(self.options) > 1:
            ax.plot(x[1:], self.log_fit_overall, label="overall")
        ax.set(xlabel="timestep (t)", ylabel="fitness", title="fitness by type")
        ax.legend()
        plt.ylim((0, 2))
        plt.show()
        if save:
            fig.savefig("fitness_num_res_")# + str(self.num_res) + "_win_" + str(self.win).replace(".", "") + "_rep_val_" + str(self.rep_val).replace(".", "") + "_options_" + str(self.options).replace(" ", "").replace(".", ""))

        #plt.stackplot(x, y_abs)
        #plt.show()

"""
game = Game()
# run for 15 timesteps
for i in range(5):
    print(i)
    game.step()
game.plot_data(save=False)
"""