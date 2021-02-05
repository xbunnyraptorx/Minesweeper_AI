import gameforai_2          #imports the game, numpy and random
import numpy as np
import random

class ai:
    def __init__(self, rows, columns, bombs):   #initializs ai board layout
        self.rows = rows                        #sets rows, columns, and bombs to what is selected
        self.columns = columns
        self.bombs = bombs
        self.totalbombs = bombs                 #saves total bomb count as self.bomb is variable
        self.board = gameforai_2.board(rows, columns, bombs)    #creates gameboard
        self.board.makeboard()                                  #makes the board
        self.prob_board = np.zeros((self.rows,self.columns), dtype=float)   #sets probability board initially to empy
        self.uncleared = self.rows*self.columns                 #uncleared spots initially at all

    def count_uncleared(self):      #function counts the number of spaces that a bomb could be
        self.uncleared = 0          #sets the number to 0 temporarily
        for x in range(self.board.rows):        #loops through every spot
            for y in range(self.board.columns):
                if self.board.viewboard[x,y] == 101:       #if the spot is the uncleared variable, it adds to it
                    self.uncleared += 1

    def bombprob(self):         #big function that assignes the probability board
        self.prob_board = np.zeros((self.rows,self.columns), dtype=float)       #resets the probability board
        self.count_uncleared()      #counts uncleared spaces
        for x in range(self.board.rows):            #loops through every spot
            for y in range(self.board.columns):
                if self.board.viewboard[x][y] != 101:       #if the spot is not a bomb, ie a marker or a 0
                    surround_count = 0              #the bomb surrounding count is intially 0

                    if x > 0 and y > 0:             #making sure not to go over the limits of the board, this function
                        if self.board.viewboard[x-1][y-1] == 101:   #counts all spaces that could be a bomb, and increases the surround count
                            surround_count += 1
                    if x > 0:
                        if self.board.viewboard[x-1][y] == 101:
                            surround_count += 1
                    if x > 0 and y < self.columns-1:
                        if self.board.viewboard[x-1][y+1] == 101:
                            surround_count += 1
                    if y < self.columns-1:
                        if self.board.viewboard[x][y+1] == 101:
                            surround_count += 1
                    if x < self.rows-1 and y < self.columns-1:
                        if self.board.viewboard[x+1][y+1] == 101:
                            surround_count += 1
                    if x < self.rows-1:
                        if self.board.viewboard[x+1][y] == 101:
                            surround_count += 1
                    if x < self.rows-1 and y > 0:
                        if self.board.viewboard[x+1][y-1] == 101:
                            surround_count += 1
                    if y > 0:
                        if self.board.viewboard[x][y-1] == 101:
                            surround_count += 1

                    if surround_count > 0:      #if the surround count is not empty, the probability at each location is assigned
                        individual_prob = int(self.board.viewboard[x,y])/surround_count

                    if x > 0 and y > 0:
                        if self.board.viewboard[x-1][y-1] == 101:
                            self.prob_board[x-1][y-1] += individual_prob
                    if x > 0:
                        if self.board.viewboard[x-1][y] == 101:
                            self.prob_board[x-1][y] += individual_prob
                    if x > 0 and y < self.columns-1:
                        if self.board.viewboard[x-1][y+1] == 101:
                            self.prob_board[x-1][y+1] += individual_prob
                    if y < self.columns-1:
                        if self.board.viewboard[x][y+1] == 101:
                            self.prob_board[x][y+1] += individual_prob
                    if x < self.rows-1 and y < self.columns-1:
                        if self.board.viewboard[x+1][y+1] == 101:
                            self.prob_board[x+1][y+1] += individual_prob
                    if x < self.rows-1:
                        if self.board.viewboard[x+1][y] == 101:
                            self.prob_board[x+1][y] += individual_prob
                    if x < self.rows-1 and y > 0:
                        if self.board.viewboard[x+1][y-1] == 101:
                            self.prob_board[x+1][y-1] += individual_prob
                    if y > 0:
                        if self.board.viewboard[x][y-1] == 101:
                            self.prob_board[x][y-1] += individual_prob

        for x in range(self.board.rows):        #for all spots that are yet to be counted, the probability is just the number of bombs
            for y in range(self.board.columns):     #still on the board vs the number of uncleared spaces
                if self.board.viewboard[x,y] == 101 and self.prob_board[x,y] == 0:
                    self.prob_board[x,y] = self.bombs/self.uncleared

    def select_min(self):       #selects the minimum probability value
        cords = []              #the coordinates of each min probability is a empty vector for now
        minval = np.min(self.prob_board[np.nonzero(self.prob_board)])   #finds the min value that is not 0 in the matrix
        for x in range(self.rows):          #loops through all spots
            for y in range(self.columns):
                if self.prob_board[x,y] == minval:      #for all spots that are that min value, add to the coordinate array
                    cords.append([x,y])
        return random.choice(cords)     #returns a random choice for coordinates with the same min value

    def startgame(self):        #plays the game
        self.board.gameplay(random.randint(0,self.rows),random.randint(0,self.columns)) #selects random starting point
        print(self.board.viewboard)     #prints the first selection board
        while self.board.boardstate == 0:       #while the board is not dead or finished
            self.count_uncleared()          #uncleared spots are counted
            if self.uncleared <= self.totalbombs:       #if the number of uncleared spots is equal to the number of bombs to start, you win
                print('You Win!!!!')
                break

            self.bombprob()     #the probability is calculated
            selection = self.select_min()       #a value is selected and inputted into the game
            self.board.gameplay(selection[0],selection[1])
            print(self.board.viewboard)     #the board is printed and bomb count decreases one
            self.bombs -= 1




new_ai = ai(4,4,2)  #starts and plays a 4x4 board with 2 bombs
new_ai.startgame()
