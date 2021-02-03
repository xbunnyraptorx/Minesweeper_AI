import random

class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []

        #fill the matrix with zeros
        for i in range(self.rows):
            self.data.append([])
            for j in range(self.cols):
                #filling the matrix with zeros as a default
                self.data[i].append(0)


    #vectorizes an input array so matrix multiplication can be done because matrix multiplication expects 2 matrices
    @staticmethod
    def vectorize(input_array):
        rows = len(input_array)

        vector = Matrix(rows, 1)

        for i in range(rows):
            vector.data[i][0] = input_array[i]

        return vector

    #takes a matrix in vector form with data like [[42],[42]] and returns [42,42]
    def matrix_vector_to_array(self):
        result = []
        for i in range(self.rows):
            result.append(self.data[i][0])
        return result

    #get out the data array
    def matrix_to_array(self):
        return self.data

    #add a random number (between -1 and 1) * mutation rate to an element in the matrix if a randomly generated number from 0 to 1 is less than the mutation rate passed in
    #should return a new matrix
    def mutate(self, mutation_rate):
        copy = self.copy()
        for i in range(copy.rows):
            for j in range(copy.cols):
                if random.uniform(0,1) < mutation_rate:
                    copy.data[i][j] += random.uniform(-1,1) * mutation_rate
        return copy


    #for matrix multiplied by matrix (matrix multiplication)
    #returns a new result matrix
    @staticmethod
    def multiply(a, b):
        if type(a) == Matrix and type(b) == Matrix:
            #check if the columns of the first one equal the rows of the second one
            #if yes, then do a matrix multiplication
            if a.cols != b.rows:
                print("The columns of the first matrix need to be equal to the rows in the second matrix")
                return None
            else:
                #make a new matrix to return
                result = Matrix(a.rows, b.cols)

                #iterate over the rows of the result matrix
                for i in range(result.rows):
                    #iterate over the columns of the result matrix
                    #we are assembling the matrix by filling in each column of the first row, then filling in each column of the second row, ...
                    for j in range(result.cols):
                        #the sum is the numnber that will be filled into the spot of the result matrix (which is where we are in the two above loops)
                        sum = 0
                        for k in range(a.cols):
                            sum += a.data[i][k] * b.data[k][j]

                        #store the sum in the spot in the result matrix
                        result.data[i][j] = sum

                #return the matrix which is the product of the two matrices
                return result
        else:
            print("Both of the arguments to this function must be matrices")
            return None


    #for elementwise and scalar multiplication
    #doesn't return anything but changes the matrix itself
    def multiply_elementwise(self, n):
        if type(n) == Matrix:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] *= n.data[i][j]
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] *= n

    #adding a copy function
    def copy(self):
        copy = Matrix(self.rows, self.cols)
        copy.setMatrix(self.data)
        return copy

    #this is a static method (can be called with Matrix.transpose(n))
    #returns the transposed matrix
    @staticmethod
    def transpose(n):
        result = Matrix(n.cols, n.rows)

        for i in range(n.rows):
            for j in range(n.cols):
                result.data[j][i] = n.data[i][j]
        return result

    #this is a transpose function that can be called with a Matrix object
    #this returns the transposed matrix and doesn't change this Matrix
    def thistranspose(self):
        result = Matrix(self.cols, self.rows)

        for i in range(self.rows):
            for j in range(self.cols):
                result.data[j][i] = self.data[i][j]
        return result

    #for matrix plus scalar or matrix plus matrix
    #changes this matrix
    def add(self, n):
        if type(n) == Matrix:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] += n.data[i][j]
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.data[i][j] += n

    #returns a new matrix
    #does this matrix minus another matrix
    def subtract(self, n):
        result = Matrix(self.rows, self.cols)
        if type(n) == Matrix:
            for i in range(self.rows):
                for j in range(self.cols):
                    result.data[i][j] = self.data[i][j] - n.data[i][j]
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    result.data[i][j] = self.data[i][j] - n
        return result

    #randomizes the numbers in the matrix to a floating point value between the two arguments
    #you can set the matrix with all equal values if you put in the same number for both parameters
    def randomize(self, lower, upper):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = random.uniform(lower, upper)

    #returns a new matrix
    def map(self, fn):
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = fn(self.data[i][j])
        return result

    #returns a new matrix
    @staticmethod
    def static_map(m, fn):
        result = Matrix(m.rows, m.cols)
        for i in range(m.rows):
            for j in range(m.cols):
                result.data[i][j] = fn(m.data[i][j])
        return result

    #takes a 2d array
    #returns a matrix
    @staticmethod
    def array_to_matrix(array):
        result = Matrix(len(array), len(array[0]))
        result.setMatrix(array)
        return result

    #sets the matrix to the values in n
    def setMatrix(self, n):
        #store these values so we don't need to keep calling the len function
        number_of_rows = len(n)
        number_of_cols = len(n[0])

        if self.rows == number_of_rows and self.cols == number_of_cols:
            for i in range(number_of_rows):
                for j in range(number_of_cols):
                    self.data[i][j] = n[i][j]
        else:
            print("Matrix values can't be set, the argument to this function must have the same shape as this matrix")
            return None

    #adding a printing functionality for easier debugging
    def print(self):
        print(self.data)
