# evolutionary-game-theory

## Requirements:
python >= 3.6  
numpy  
matplotlib   

## Explanation of variables:
num_res: number of foodsources

win: the payoff matrix.

population: starting population. Denote hawk by [1], dove by [2] and a mixed strategy that plays hawk with probability p and dove with probability 1-p by [1-p, p].

rep_val: reward needed for reproduction. I.e. if rep_val=0.5: having reward of 1 keeps me alive (0.5) and allows me the reproduce once (additional 0.5).

## Plots
There are 4 plot avaiable: total population size, total populationsize by type of individual, relative size of population by type, average fitness by type.  
To save the plot ru plot_data with save = True  

## Remarks
If there are more than two times the amount of individuals than food sources, i.e. some individuals will not be able to get a spot, then this individuals will die.  
Fitness is defined as the expected reward of all individuals of a certain type that were able to get a spot at a food source.  
For population size by type an relative population, only the individuals that got a spot are considered.  
All values in "win" should be a multiple of "rep_val".  

