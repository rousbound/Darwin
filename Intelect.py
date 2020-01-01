import random
import numpy as np

class Network(object):

    # Resume of transformations
    # sizes = [8,9,15,3]
    # total_weight = 252 ( 8*9 + 9*15 + 15 * 3)
    # sizePairs = [[9,8],[15,9],[3,15]]
    # synapsesLayersCount = [72,125,45]
    # synapsesLayersWeights = [72weights,125weights,45weights]
    # neuronsSynapses = [[9,8weights],[15,9weights],[3,15weights]]

  
    def __init__(self, sizes,weights = None,from_array = None):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.sizePairs = [[x,y] for (x,y) in zip(self.sizes[1:],self.sizes[:-1])]
        #print(self.sizePairs)

        if np.any(weights):
            self.weights = weights
        else:
            self.weights = np.random.rand(self.get_total_weights())
        self.neuronsSynapses = self.decode_weights()


    def get_total_weights(self):
        self.mult = [[x*y] for (x,y) in zip(self.sizes[1:],self.sizes[:-1])]
        self.total = 0
        for mulResult in self.mult:
            self.total += mulResult[0]
        return self.total

    def decode_weights(self):
        self.synapsesLayersCount = [x[0]*x[1] for x in self.sizePairs]
        self.synapsesLayersWeights = []

        for x in self.synapsesLayersCount:
            length = len(self.synapsesLayersWeights)
            self.synapsesLayersWeights.append(self.weights[length:length+x])
        
        neuronsSynapses = []
        for x,y in zip(self.synapsesLayersWeights,self.sizePairs):
            a = x.reshape(y[0],y[1])
            neuronsSynapses.append(a)
        return neuronsSynapses


    def feedforward(self, a):
        # Feedforward except in the final layer
        for w in self.neuronsSynapses[:-1]:
            a = np.tanh(np.matmul(w,a))
        w = self.neuronsSynapses[-1]
        z = np.matmul(w,a)
        a = softmax(z)
        return a

def softmax(z):
    s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)
    return s

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

#net = Network([8,9,15,3])
#net.decode_weights()
