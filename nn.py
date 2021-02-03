import matrix2d
import math

class NeuralNetwork:
    def __init__(self, shape, learning_rate = 0.1, data = [[],[]], mutation_rate = 0.1):

        #get the shape as a two dimensional array
        self.shape = shape

        #get the length of self.shape so we don't need to repeatedly call the len function
        self.len_selfshape = len(self.shape)

        #save the mutation rate
        self.mutation_rate = mutation_rate

        #save these so we don't need to keep performing operations which will always have constant value
        self.len_selfshape_minus_1 = self.len_selfshape - 1
        self.len_selfshape_minus_2 = self.len_selfshape - 2

        #store an activation function
        #ADD YOUR OWN ACTIVATION FUNCTION BELOW THEN CHANGE self.activation_function to be equal to the name of your activation function
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))

        def nothing(x):
            return x

        def relu(x):
            if x <= 0:
                return 0
            else:
                return x

        # #this should really be return sigmoid(x) * (1- sigmoid(x))
        # #but the output of each layer has already been fed through the sigmoid function
        def dsigmoid(y):
            return y * (1 - y)

        # def twice(x):
        #     return x*2

        self.activation_function = relu
        self.activation_function_derivative = dsigmoid

        #set the learning rate
        #default is 0.1
        self.lr = learning_rate

        #initialize the container weights array
        #this will store all of the matrices needed (from the matrix2d.py library)
        self.weight_matrices = []
        #if there are saved weights, they are added here
        if data != [[],[]]:
            for i in range(self.len_selfshape_minus_1):
                self.weight_matrices.append(matrix2d.Matrix.array_to_matrix(data[0][i]))

        #initialize the container bias array
        #this will store all of the biases for all of the neurons (organized in matrices)
        self.bias_matrices = []
        #if there are saved biases, they are added here
        if data != [[],[]]:
            for i in range(self.len_selfshape_minus_1):
                self.bias_matrices.append(matrix2d.Matrix.array_to_matrix(data[1][i]))

        if data == [[],[]]:
            #interate over every neuron layer in the neural net
            for i in range(self.len_selfshape_minus_1):
                #add a matrix to the weights matrix
                #keep in mind that it is added to the end of the bigger array
                #the weight matrix has rows equal to the number of nodes in the next layer, and columns equal to the number of inputs coming in
                self.weight_matrices.append(matrix2d.Matrix(self.shape[i + 1][0], self.shape[i][0]))

                #set random weights between -1 and 1
                self.weight_matrices[i].randomize(-1,1)

                #add a bias vector (a Matrix object) to the bias_matrices container array
                #should have rows equal to the number of neurons in the next layer and one column (because it is a vector)
                self.bias_matrices.append(matrix2d.Matrix(self.shape[i + 1][0], 1))

                #set random biases between -1 and 1
                self.bias_matrices[i].randomize(-1,1)
        else:
            pass

        #create an array with all of the transposed weight matrices(rows of original matrix = columns of transposed matrix)
        #we are doing it once so that we don't have to keep transposing all of the weight matrices whenever we call the train function
        self.weight_matrices_transposed = []

        for i in range(self.len_selfshape_minus_1):
            self.weight_matrices_transposed.append(matrix2d.Matrix.transpose(self.weight_matrices[i]))

        #we are reversing the transposed weight matrices array because we need to iterate backwards through the network
        #we need to use the last weights of the network first so we can backpropagate the error
        self.weight_matrices_transposed.reverse()

        #has a score and probability of being picked when used with a genetic algorithm
        self.score = None
        self.probability = None

    #get an array with the neural network's data
    def get_data(self):
        data = [[],[]]
        for i in range(self.len_selfshape_minus_1):
            data[0].append(self.weight_matrices[i].matrix_to_array())
            data[1].append(self.bias_matrices[i].matrix_to_array())

        return data

    #lots of matrix math
    #takes the inputs and feeds it through the network
    def feedforward(self, input_arr):
        #turn the input array into an input matrix
        inputs = matrix2d.Matrix.vectorize(input_arr)

        #iterate over every time we need to do Output = activation_function(Weight_matrix * Input_matrix + Bias_vector)
        #we need to do this every gap between layers (which is the numbers of layers we have - 1)
        for i in range(self.len_selfshape_minus_1):

            weighted_sum = matrix2d.Matrix.multiply(self.weight_matrices[i], inputs)
            weighted_sum.add(self.bias_matrices[i])
            inputs = weighted_sum.map(self.activation_function)

        #every loop iteration, the inputs to the layer becomes the inputs to the next layer in the network
        #then the last inputs are inputs to the output
        #returns a two dimensional array with all the data of the matrix
        return inputs.matrix_vector_to_array()

    #should randomly add small changes in the weights and biases of the neural network based on the mutation rate
    #returns a copy of the mutated network
    def mutate(self):
        c = self.copy()
        for i in range(c.len_selfshape_minus_1):
            c.bias_matrices[i] = c.bias_matrices[i].mutate(c.mutation_rate)
            c.weight_matrices[i] = c.weight_matrices[i].mutate(c.mutation_rate)

        return c

    #copy the network
    #why am I using matrix_vector_to_array, the wieght matrices are 2d!
    def copy(self):
        data = [[],[]]
        for i in range(self.len_selfshape_minus_1):
            data[0].append(self.weight_matrices[i].copy().matrix_to_array())
            data[1].append(self.bias_matrices[i].copy().matrix_to_array())

        return NeuralNetwork(self.shape, learning_rate = self.lr, mutation_rate = self.mutation_rate, data = data)


    #the train function should use backpropagation and gradient descent to change the weights of the network
    #useful for supervised learning (where you have labels for data)
    #arguments should both be arrays and one dimensional (vectors)
    def train(self, inputs, targets):

        #turn the input array into an input matrix
        inputs = matrix2d.Matrix.vectorize(inputs)

        #make an array to contain all of the transposed outputs of the layers except the last layer
        #needed for calculating change in weights
        layer_outputs_transposed = []
        #layer_outputs will store the outputs of all of the layers except for the input layer
        #we will use this with the derivative of sigmoid to help calculate the change in weights
        layer_outputs = []
        #get the ouput of the input layer (which is the input) and transpose it
        layer_outputs_transposed.append(matrix2d.Matrix.transpose(inputs))

        #iterate over every time we need to do Output = activation_function(Weight_matrix * Input_matrix + Bias_vector)
        #we need to do this every gap between layers (which is the numbers of layers we have - 1)
        for i in range(self.len_selfshape_minus_1):

            weighted_sum = matrix2d.Matrix.multiply(self.weight_matrices[i], inputs)

            weighted_sum.add(self.bias_matrices[i])

            inputs = weighted_sum.map(self.activation_function)

            #save the layer outputs if it isn't the first inputs
            layer_outputs.append(inputs)

            #save the transposed version if it isn't the final output
            #we don't need the final ouput transposed for the backpropagation
            #we only need the transposed outputs of the layers before
            #i will be equal to self.len_selfshape - 2 during the last iteration
            if i != (self.len_selfshape_minus_2):
                layer_outputs_transposed.append(matrix2d.Matrix.transpose(inputs))
            else:
                pass

        #the layer outputs and the transposed versions need to start with the last outputs for a backpropagation loop
        layer_outputs.reverse()
        layer_outputs_transposed.reverse()

        #make an array to store all of the error values for all the nodes
        errors = []

        #make the targets into a matrix so we can subtract the neural network's guess from it to get the error
        targets_matrix = matrix2d.Matrix.vectorize(targets)

        #error = targets - guess
        #inputs is the last mapped weighted sum from the feedforward step
        #the difference from this to the feedforward function is that we want to keep the network's ouput as a matrix
        errors.append(targets_matrix.subtract(inputs))

        #calculate all of the error matrices for all of the layers and save them in the errors array
        #the transposed weight matrix times the error matrix (vector) of the forward layer equals the error matrix of this layer
        for i in range(self.len_selfshape_minus_2):
            errors.append(matrix2d.Matrix.multiply(self.weight_matrices_transposed[i], errors[i]))

        #calculate the change in weight matrices and the change in bias matrices
        #going backwards through the network
        #change in weight matrix = learning rate scalar times error vector of the layer in front elementwise multiplied by the derivative of the activation function with forward layer's outputs then matrix multiplied by the transposed outputs of the behind layer
        #change in bias matrix = learning rate scalar times error vector of forward layer elementwise multiplied by the derivative of the activation function with forward layer
        #https://github.com/ProWhalen/AndrewNg-ML/blob/master/Make%20Your%20Own%20Neural%20Network.pdf has a lot more information and a much better explanation
        for i in range(self.len_selfshape_minus_1):
            #my method for gradient descent and calculating the gradient
            #gradient = errors[i].copy()
            #gradient.multiply_elementwise(layer_outputs[i])
            #gradient.multiply_elementwise(self.lr)

            #maping the outputs of the layer in front with the derivative
            gradient = matrix2d.Matrix.static_map(layer_outputs[i], self.activation_function_derivative)
            #scaling by the learning rate
            gradient.multiply_elementwise(self.lr)
            #multiply by the errors of the layer in front
            gradient.multiply_elementwise(errors[i])

            #the change in biases is the gradient here
            self.bias_matrices[self.len_selfshape - (2 + i)].add(gradient)

            #calculate the change in weights
            #multiplying the gradient calculated above by the transposed outputs of the layer behind
            weight_deltas = matrix2d.Matrix.multiply(gradient, layer_outputs_transposed[i])

            #the weight_matrices start from the inputs to the first hidden layer
            #we are going backward through the network
            self.weight_matrices[self.len_selfshape - (2 + i)].add(weight_deltas)

        #REMEMBER TO CHANGE THE TRANSPOSED WIEGHT MATRICES AFTER NEW WEIGHTS ARE CALCULATED
        #for error backpropagation
        for i in range(self.len_selfshape_minus_1):
            self.weight_matrices_transposed[i] = matrix2d.Matrix.transpose(self.weight_matrices[i])

        #AND REMEMBER TO REVERSE IT
        self.weight_matrices_transposed.reverse()

        return errors[0].matrix_vector_to_array()



    #prints the shape of the neural net and all of its weights and biases and activation function
    def print(self):
        print("Shape: " + str(self.shape))
        print()
        print("Weights:")
        for i in range(self.len_selfshape - 1):
            print(self.weight_matrices[i].data)
        print()
        print("Biases: ")
        for i in range(self.len_selfshape - 1):
            print(self.bias_matrices[i].data)
        print()
        print("Activation function: " + str(self.activation_function))
