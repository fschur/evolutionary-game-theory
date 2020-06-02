from hawk_dove_game_new import Game
import numpy as np

win_1 = [[0,0,0,0,0],
         [2,1,0,0,1],
         [2,2,0.4,2,0.4],
         [2,2,0,0.4,0.4],
         [2,1,0.4,0.4,1]]

win_2 = [[0,2,2,2,2],
         [0,1,2,2,1],
         [0,0,0.4,0,0.4],
         [0,0,2,0.4,0.4],
         [0,1,0.4,0.4,1]]

win = [np.array(win_1), np.array(win_2)]

lookup = {"[0]": "emtpy", "[1]": "dove", "[2]": "hawk", "[3]": "snitch", "[4]": "robin hood"}

game = Game(lookup=lookup ,num_res=20000, win=win,
            population=[[1]]*20000 + [[2]]*5000 + [[3]]*5000 + [[4]]*5000, rep_val=0.5)
timesteps = 50

for i in range(timesteps):
    print(i)
    game.step()
game.plot_data(save=False)
