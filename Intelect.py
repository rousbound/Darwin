import random
import numpy as np

class Network(object):

    def __init__(self, sizes,weights = None,from_array = None):
        self.num_layers = len(sizes)
        self.original_sizes = sizes
        self.sizes = [[x,y] for (x,y) in zip(sizes[1:],sizes[:-1])]
        #print("sizes:",self.sizes)
        if np.any(weights):
            self.weights = weights
            #print("from weights")
            self.shaped = self.decode_weights()
        else:
            self.weights = np.random.rand(self.get_total_weights())
            self.shaped = self.decode_weights()


    def get_total_weights(self):
        self.mult = [[x*y] for (x,y) in zip(self.original_sizes[1:],self.original_sizes[:-1])]
        self.total = 0
        for i in self.mult:
            self.total += i[0]
        return self.total

    def decode_weights(self):
        self.unshaped = [x[0]*x[1] for x in self.sizes]
        self.unshaped2 = []
        for x in self.unshaped:
            self.unshaped2.append(self.weights[:x])
        self.shaped = []
        for x,y in zip(self.unshaped2,self.sizes):
            a = x.reshape(y[0],y[1])
            self.shaped.append(a)
        return self.shaped

    def feedforward(self, a):
        #print("shaped",self.final)
        for w in self.shaped[:-1]:
            a = np.tanh(np.matmul(w,a))
        w = self.shaped[-1]
        z = np.matmul(w,a)
        a = softmax(z)
        return a

def softmax(z):
    s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)
    return s

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

#net = Network([8,10,10,4])
#net.decode_weights()
