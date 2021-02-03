#import libraries
import nn
import ga
import random
import numpy as np
import gameforai
import math

#have global storing variables
#POPSIZE is how many networks in each generation
POPSIZE = 100
#make a variable to hold the number of generations
num_of_gens = 0
#make an array to hold all of the nets
nets = []

gen_inputs = []     #matrix of total boards
new_board = []      #empty vector for new boards

__sum = 0           #sets intial sum value to 0



#make a fitness function that will return a score for the network based on how well it did
#higher is better
def evaluateNetwork(net):
    __sum = 0
    for i in range(len(gen_inputs)):
        #keeps playing the game until it is dead or finished
        while gen_inputs[i].boardstate == 0:
            #sets the input to the game to the output of the NN, the inputs of which are the current viewed board, flattened
            [x,y] = net.feedforward(gen_inputs[i].viewboard.flatten())
            #plays the game with those x and y inputs
            gen_inputs[i].gameplay(x,y)
        __sum += gen_inputs[i].score
    return __sum


#make an evolve function
def evolve():
    #use the global variables
    global num_of_gens
    global nets
    global POPSIZE
    global gen_inputs
    global __sum

    __sum = 0

    print(num_of_gens)

    #resets these two to empty if not already
    gen_inputs = []
    new_board = []

    #creates a gameboard for each number of the population
    for i in range(POPSIZE):
        #new board is emptied
        new_board = []
        #newboard is the gameboard and it places the bombs
        new_board = gameforai.board(8,8,10)
        new_board.makeboard()
        #adds the new board to the vector of all boards
        gen_inputs.append(new_board)

    #if it is the first generation, create the first nets
    if num_of_gens == 0:
        nets.append([])
        for i in range(POPSIZE):
            nets[0].append(nn.NeuralNetwork([[64],[10],[10],[2]]))

    #loop through all of the nets of the current generation

    for net in nets[num_of_gens]:
        net.score = evaluateNetwork(net)
        #print(str(nets[num_of_gens].index(net)) + ' / ' + str(POPSIZE))
    #get ready to spawn the next generation
    nets.append([])

    #make the probabilities for the networks to be picked
    nets[num_of_gens + 1].extend(ga.nextGeneration(nets[num_of_gens]))


    #increment the number of generations
    num_of_gens += 1




#run evolve certain number of times
def runEvolve(n):
    for i in range(n):
        evolve()

#run 25 epochs
runEvolve(25)

#outputs the last board with that particular net
while gen_inputs[0].boardstate == 0:
    [x,y] = nets[num_of_gens][0].feedforward(gen_inputs[i].viewboard.flatten())
    gen_inputs[0].gameplay(x,y)
print(gen_inputs[0].viewboard)
