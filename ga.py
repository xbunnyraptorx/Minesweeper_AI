#genetic algorithm functions
#inspired by Dan Shiffman and the coding train
#Simon Socolow 2020
import random


#generates the next generation based on the previous generation and returns it
#relies on the previous generation having a mutate function
def nextGeneration(pgen):
    #calculate their fitness
    calculateFitness(pgen)
    #make an array for the next generation
    ngen = []
    #add to the next generation agents that were picked by the pickOne function and then mutate them
    for individual in pgen:
        ngen.append(pgen[pickOne(pgen)].mutate())
    #return the next generation
    return ngen

#takes an array with objects that have a probability property and picks one based on its probability in an ingenious way (found on coding train's github) (https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_100.1_NeuroEvolution_FlappyBird/P5/ga.js)
#returns the index of the chosen one in the list
def pickOne(list_):
    #start the index at 0
    index = 0
    #generate a random number between 0 and 1
    r = random.random()
    #while that number is greater than 0 (still positive), subtract from it an agent's probablility and increment the index
    #then it returns 1 more than the index of the agent that made r go negative
    while r > 0:
        r = r - list_[index].probability
        index = index + 1
    #subtract 1 to get back to the right index
    index = index - 1
    #return that index
    return index

#takes an array with probabilities (numbers between 0 and 1 that sum to 1) and picks one based on its probability in an ingenious way (found on coding train's github) (https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_100.1_NeuroEvolution_FlappyBird/P5/ga.js)
#returns the index of the chosen one in the list
def pickOneProbs(list_):
    #start the index at 0
    index = 0
    #generate a random number between 0 and 1
    r = random.random()
    #while that number is greater than 0 (still positive), subtract from it an agent's probablility and increment the index
    #then it returns 1 more than the index of the agent that made r go negative
    while r > 0:
        r = r - list_[index]
        index = index + 1
    #subtract 1 to get back to the right index
    index = index - 1
    #return that index
    return index

#takes an array of numbers as input
#outputs an array of probabilities that correspond with those numbers
def makeProbs(array):
    sum_ = 0
    probs = []
    for n in array:
        sum_ += n
    for n in array:
        probs.append(n / sum_)
    return probs

#takes an array of objects with a score property and assigns a probability value to their probability property
def calculateFitness(list_):
    sum_ = 0
    for obj in list_:
        sum_ += obj.score
    for obj in list_:
        obj.probability = obj.score / sum_