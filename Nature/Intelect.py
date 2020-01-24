import numpy as np

class Network(object):

    # Variables dictionary
    # sizes = [8,9,15,3]
    # total_weight = 252 ( 8*9 + 9*15 + 15 * 3)
    # sizePairs = [[9,8],[15,9],[3,15]]
    # synapsesOfEachLayer = [72,125,45]
    # layerWeights = [72weights,125weights,45weights]
    # synapsesOfEachNeuron = [[9,8weights],[15,9weights],[3,15weights]]

  
    def __init__(self, sizes,weights = None,from_array = None):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.sizePairs = [[x,y] for (x,y) in zip(self.sizes[1:],self.sizes[:-1])]

        if np.any(weights):
            self.weights = weights
        else:
            self.weights = np.random.rand(self.get_total_weights())

        self.synapsesOfEachNeuron = self.decode_weights()


    def get_total_weights(self):
        self.mult = [x*y for (x,y) in zip(self.sizes[1:],self.sizes[:-1])]
        return sum(self.mult)

    def decode_weights(self):
        self.synapsesOfEachLayer = [x[0]*x[1] for x in self.sizePairs]
        synapsesOfEachNeuron = []
        pointer = 0
        for synapsesOfLayer, sizePair in zip(self.synapsesOfEachLayer, self.sizePairs):
          layerWeights = self.weights[pointer : pointer + synapsesOfLayer]
          layerWeights = layerWeights.reshape(sizePair[0],sizePair[1])
          synapsesOfEachNeuron.append(layerWeights)
          pointer += synapsesOfLayer
            
        return synapsesOfEachNeuron

    def feedforward(self, a):
        # Feedforward except in the final layer
        for w in self.synapsesOfEachNeuron[:-1]:
            a = np.tanh(np.matmul(w,a))
        w = self.synapsesOfEachNeuron[-1]
        z = np.matmul(w,a)
        a = softmax(z)
        return a

# The softmax function is an activation function that turns numbers into probabilities which sum to
# one. Softmax function turns logits [2.0, 1.0, 0.1] into probabilities [0.7, 0.2, 0.1], and the
# probabilities sum to 1

# ndarray.T: Same as self.transpose(), except that self is returned if self.ndim < 2.
# np.exp(x): e**x
# reshape(-1,1): reshape matrix with one column and an unspecified number of rows that make the
# reshaping compatible
def softmax(z):
    s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)
    return s

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

#net = Network([8,9,15,3])
#net.decode_weights()
