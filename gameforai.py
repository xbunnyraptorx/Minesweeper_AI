import numpy as np                                                              #imports librarires
import random

class board:                                                                    #makes board
    def __init__(self, rows, columns, bombs):                                   #intializes variables with inputs for rows/columns and bombs
        self.rows = rows
        self.columns = columns
        self.bombs = bombs
        self.board = []                                                         #initializes blank board
        self.viewboard = np.full((self.rows,self.columns),101, dtype=int)       #initializs board that is seen
        self.visited = np.zeros((self.rows,self.columns), dtype=int)            #matrix if the player has already visited
        self.boardstate = 0                                                     #0 if the game is still in play, 1 if the game is over
        self.score = 1/(self.rows*self.columns)                                 #sets score as the inverse of the number of unrevealed blocks

    def makeboard(self):                                                        #function to make board
        a = np.zeros((self.rows,self.columns), dtype=int)                       #makes integer board of 0s to start
        boardbombs = self.bombs                                                 #makes a copy of self.bombs to use in this while loop

        while boardbombs > 0:                                                   #loop positions all bombs, keeps iterating until all bombs are used
            for x in range(self.rows):
                for y in range(self.columns):                                   #a number of bombs/total slots chance to place a bomb
                    if a[x][y] == 0 and random.random() < (boardbombs/(self.rows*self.columns)) and boardbombs > 0:
                        a[x][y] = -1
                        boardbombs -= 1

        bombcount = 0                                                           #intializes bombcount variable
        for x in range(self.rows):                                              #loops through all rows and columns
            for y in range(self.columns):
                if a[x][y] == 0:                                                #if the current square is not already marked as a bomb
                    if x > 0 and y > 0:                                         #bombcount increases for all adjacent bombs to the square in question
                        if a[x-1][y-1] == -1:                                   #making sure to not iterate beyond the bounds of the matrix
                            bombcount += 1
                    if x > 0:
                        if a[x-1][y] == -1:
                            bombcount += 1
                    if x > 0 and y < self.columns-1:
                        if a[x-1][y+1] == -1:
                            bombcount += 1
                    if y < self.columns-1:
                        if a[x][y+1] == -1:
                            bombcount += 1
                    if x < self.rows-1 and y < self.columns-1:
                        if a[x+1][y+1] == -1:
                            bombcount += 1
                    if x < self.rows-1:
                        if a[x+1][y] == -1:
                            bombcount += 1
                    if x < self.rows-1 and y > 0:
                        if a[x+1][y-1] == -1:
                            bombcount += 1
                    if y > 0:
                        if a[x][y-1] == -1:
                            bombcount += 1

                    a[x][y] = bombcount                                         #the square is labled with the number of bombs surrounding
                    bombcount = 0
        self.board = a                                                          #the board variable is assigned to the new matrix of a

    def clearneighbors(self,x,y):                                               #recursive function to clear the spot the player is on and any adjacent
                                                                                #spots that are 0s
        if self.board[x,y] == 0 and self.visited[x,y] == 0:                     #if the spot has not already been visited
            self.viewboard[x,y] = self.board[x,y]                               #the spot is changed to its real value
            self.visited[x][y] = 1                                              #the visited value is changed to true

            if x > 0 and y > 0:                                                 #all 0 neighbors are also called and cleared
                self.clearneighbors(x-1,y-1)
            if x > 0:
                self.clearneighbors(x-1,y)
            if x > 0 and y < self.columns-1:
                self.clearneighbors(x-1,y+1)
            if y < self.columns-1:
                self.clearneighbors(x,y+1)
            if x < self.rows-1 and y < self.columns-1:
                self.clearneighbors(x+1,y+1)
            if x < self.rows-1:
                self.clearneighbors(x+1,y)
            if x < self.rows-1 and y > 0:
                self.clearneighbors(x+1,y-1)
            if y > 0:
                self.clearneighbors(x,y-1)

        else:
            self.viewboard[x,y] = self.board[x,y]                               #in any other case, the board is set to that value

    def gameplay(self,x,y):
            x = int(round(self.rows*x/20000))                                   #sets x and y as the output from the NN, scaled by an arbitrary number
            y = int(round(self.columns*y/20000))

            if self.visited[x,y] == 1 or self.board[x,y] == -1:                 #if the spot it choses has already been seen or is a bomb, genocide
                self.score = 1/(self.rows*self.columns)
                self.boardstate = 1

            blankcount = np.count_nonzero(self.viewboard == 101)                #counts number of spots uncleared
            if blankcount <= self.bombs:                                        #if the number of blanks is the number of bombs, the game is won, score increases by 100
                self.score == 100
                self.boardstate = 1

            if self.visited[x][y] == 0 and self.board[x,y] != -1:               #otherwise, if the spot is not visited and the spot it chose is not a bomb, the score increases
                self.clearneighbors(x,y)
                self.score = 100/blankcount

            self.visited[x,y] = 1                                               #sets current spot to visited (if not already redundant)
