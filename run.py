from hawk_dove_game import Game


game = Game(num_res=20000, win={"dove": [1, 0.5, 2], "hawk": [0.6, 1.5, 2]},
            population=[[1, 0]]*39990 + [[0, 1]]*10, rep_val=0.1)
timesteps = 40

for i in range(timesteps):
    game.step()
game.plot_data(save=False)