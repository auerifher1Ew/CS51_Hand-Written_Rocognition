# Recognition.py
#
# This will by the file that contains the methods and algorithms for
# recognizing our characters obtained via object separation. It will use
# the NIST database for our training data.
#
#
#
#

# import libraries for handling randomness and numerical operations
import random
import numpy as np
import json
import sys
import Data
# TODO: Make a method for testing and conveniently displaying the
# the success of our training network


class QuadCost:

    # gives cost of calculated output a and actual output y
    @staticmethod
    def fn(a, y):
        return 0.5*np.linalg.norm(a-y)**2

    # returns change in error from the output layer
    @staticmethod
    def delta(z, a, y):
        return (a-y) * sigm_deriv_vector(z)


class CrossEntropyCost:

    # Returns the cost of the calculated output a with actual output y
    # np.nan_to_num covers the case of nan as an output.
    @staticmethod
    def fn(a, y):
        return np.sum(np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)))

    # returns the difference between output and actual output
    @staticmethod
    def delta(z, a, y):
        return (a-y)


class Recognition ():

    # steps to be taken when the network is initialized
    def __init__(self, layers, cost=CrossEntropyCost):

        # store the size and dimensions of the network in the object
        self.width = len(layers)
        self.layers = layers

        # initialize the bias and weight lists
        self.biases = []
        self.weights = []
        self.cost = cost

        # the biases are not present in the first layer,
        # but then match the size of following layers
        # initialize with random Guassian Values
        for i in self.layers[1:]:
            self.biases.append(np.random.randn(i, 1))

        # the biases are matrcies that allow matrix multiplication
        # by the input vector to be carried through to the output later.
        # initialized with n^(-.5) Guassian values
        for a, b in zip(self.layers[:-1], self.layers[1:]):
            self.weights.append(np.random.randn(b, a)/np.sqrt(a))

    # step_net(self, xs) will take a layer of the neural network and return the
    # output layer. It uses the the sigmoid function
    # and weights and biases to calculate the next activations
    def step_net(self, xs):
        for b, w in zip(self.biases, self.weights):
            xs = sigm_vector(np.dot(w, xs) + b)
        return xs

    # training function using the gradient descent method to find the
    # minimum of our "cost" function. This will either operate on a small
    # sample of the larger training set (stochastically) or on a predetermined
    # set. The training data will be a list of tuples with
    # (input image, expected outcome) format"""
    def train(self, training_set, num_runs, sample_size, training_param,
              test_data=None, reg_param=0.0):

        # get size of training data
        n_tr_sets = len(training_set)

        # for each training session, build randomly chosen training sets
        # from the training data, then update the network.
        for i in xrange(num_runs):

            # shuffle the training data
            random.shuffle(training_set)

            # make samples from training data
            samples = []
            for j in xrange(0, n_tr_sets, sample_size):
                samples.append(training_set[j:j + sample_size])

            # for each sample, update the network
            for samp in samples:
                self.update_sample(
                    samp, training_param, reg_param, len(training_set))

            # if there is testing data, print the results at this stage
            if test_data:
                print "Session {0}: {1}".format(i, self.results(test_data))
            else:
                print "Session {0} complete".format(i)

    # update_sample is a method to update the weights and biases of the network
    # given a sample from training data and the training paramete.
    # it will use the gradient found with backpropagation.
    def update_sample(self, sample, training_param, reg_param, n_train):

        del_b = [np.zeros(b.shape) for b in self.biases]
        del_w = [np.zeros(w.shape) for w in self.weights]
        for xs, ys in sample:
            ddel_b, ddel_w = self.grad_bp(xs, ys)
            del_b = [db + ddb for db, ddb in zip(del_b, ddel_b)]
            del_w = [dw + ddw for dw, ddw in zip(del_w, ddel_w)]
        self.weights = [
            (1-training_param*(reg_param/n_train))*w-(training_param/len(sample))*nw
            for w, nw in zip(self.weights, del_w)]
        self.biases = [b - (training_param / len(sample)) * nb
                       for b, nb in zip(self.biases, del_b)]

    # make the gradient of the cost function using the method of
    # backpropogation. This returns a tuple representing the
    # partials wrt weights and biases
    def grad_bp(self, x, y):

        # initialize the gradient arrays
        del_b = [np.zeros(b.shape) for b in self.biases]
        del_w = [np.zeros(w.shape) for w in self.weights]

        # initialize the activation with the input and make lists for the
        # activations and z layer.
        activ = x
        activs = []
        activs.append(activ)
        zs = []

        # calculate the rest of the activations and z layers and add them to
        # our lists
        for (b, w) in zip(self.biases, self.weights):
            # next z value
            z = np.dot(w, activ) + b
            # add to list of zs
            zs.append(z)
            # next activation
            activ = sigm_vector(z)
            # add to list of activations
            activs.append(activ)

        # calcualte the error (change) between the predicted output and actual
        # output
        error = (self.cost).delta(zs[-1], activs[-1], y)
        del_b[-1] = error
        del_w[-1] = np.dot(error, activs[-2].transpose())

        # carry our calculated error back through the network via
        # backpropagation
        for l in xrange(2, self.width):
            z = zs[-l]
            error = np.dot(
                self.weights[-l + 1].transpose(), error) * sigm_deriv_vector(z)
            del_b[-l] = error
            del_w[-l] = np.dot(error, activs[-l - 1].transpose())

        return (del_b, del_w)

    # takes a test set (list of tuples) and returns the ratio of tuples
    # identified correctly.
    def results(self, testing_set):
        # init results
        tst_rslts = []

        # run testing set through the network with step_forward
        for x, y in testing_set:
            tst_rslts.append((np.argmax(self.step_net(x)), np.argmax(y)))

        # define number of correct identifications as a ratio
        success = sum(float(x == y) for (x, y) in tst_rslts)/len(testing_set)

        # return the ratio
        return success

    # save the neural network for later use with given savename
    def save(self, savename):
        network = {"layers": self.layers,
                   "weights": [w.tolist() for w in self.weights],
                   "biases": [b.tolist() for b in self.biases],
                   "cost": str(self.cost.__name__)}
        f = open(savename, 'w')
        json.dump(network, f)
        f.close()

    # function to perform recognition on actual data
    def recognize(self, real_data):
        data = Data.extracted_load(real_data)
        # initialize the output character list
        string = ''
        init_ltr = str(unvectorize_output(self.step_net(data[0][0])))
        string = string + init_ltr
        row_ctr = 0
        print data[0][0]
        for i in xrange(1, len(data)):
            ltr = str(unvectorize_output(self.step_net(data[i][0])))
            if data[i][1][0] > row_ctr:
                string = string + '\n' + ltr
                row_ctr = row_ctr + 1
            elif data[i][1][1] == 0:
                string = string + " " + ltr
            else:
                string = string + ltr
        return string


# load a premade network from a file named filename
def load(filename):

    f = open(filename, 'r')
    network = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], network["cost"])
    net = Recognition(network["layers"], cost=cost)
    net.weights = [np.array(weight) for weight in network["weights"]]
    net.biases = [np.array(bias) for bias in network["biases"]]

    return net


# sigmoud functions that characterize the transition between nodes.
def sigm(z):
    return 1.0 / (1.0 + np.exp(-z))

sigm_vector = np.vectorize(sigm)


def sigm_deriv(z):
    return sigm(z) * (1 - sigm(z))

sigm_deriv_vector = np.vectorize(sigm_deriv)


# converts the output array from the network to a char
def unvectorize_output(output_vec):
    ltr_ind = np.argmax(output_vec)
    if 0 <= ltr_ind <= 25:
        return chr(ltr_ind + ord('A'))
    elif 26 <= ltr_ind <= 51:
        return chr((ltr_ind - 26) + ord('a'))
