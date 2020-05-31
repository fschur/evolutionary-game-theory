# evolutionary-game-theory

## Requirements:
python >= 3.6
numpy
matplotlib

## Explanation of variables:
num_res: number of foodsources

win: describes the game-table as a python dictionary: First entry is the reward when playing against the same kind of individual (dove, dove; hawk,hawk), second is the reward if playing against the opposing kind of individual, last entry is the reward for arriving at a food-resource alone.

population: starting population. Denote Hawk by [0,1], dove by [1, 0] and a mixed strategy that plays hawk with probability p and dove with probability 1-p by [1-p, p] 

rep_val: reward needed for reproduction. I.e. if rep_val=0.5: having reward of 1 keeps me alive (0.5) and allows me the reproduce once (additional 0.5).


## Remarks
rep_val win
more than resouc
save
