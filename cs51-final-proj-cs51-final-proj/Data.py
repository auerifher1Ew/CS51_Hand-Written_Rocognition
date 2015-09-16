# Data.py
#
#
# This will be the module that handles the data we need for testing and training our neural network.
# It will also deal with the extracted objects of the actual data
#
#
# load necessary libraries
# from scipy import ndimage
# from scipy import misc
# import matplotlib.pyplot as plt
# import os
import numpy as np
import cPickle
import random


""" function to open the file containing MNIST data and return training data, test data,
    and validation data in a tuple
def num_load(): (training_data, testing_data, validation_data)
# open file containing desired data
# load data into variables (np_arrays or similar structures) with cPickle library or similar
# reshape data as desired to pass into recognition.py
# close the file
# return the tuple of variables"""


def alpha_load():

    # load raw testing and training sets
    f = open('alphabets2.pkl', 'rb')
    u_data, l_data = cPickle.load(f)
    f.close()

    # use our dividing function to get a training and testing set
    train_set, test_set = divide_data(u_data, l_data)

    # init new data sets (list of input arrays, list our output vector)
    training_data = []
    testing_data = []

    # reshape training and testing data to fit our neural network better
    for alph in train_set:
        for im, ltr in alph:
            training_data.append((np.reshape(im, (784, 1)),
                                 output_vec(ltr)))
    for test_list in test_set:
        for array, output in test_list:
            testing_data.append((np.reshape(array, (784, 1)),
                                output_vec(output)))

    # return newly formatted data
    return (training_data, testing_data)


def divide_data(u_data, l_data):

    # define size of data sets
    test_size = 200

    # randomly shuffle
    random.shuffle(u_data)
    random.shuffle(l_data)

    u_test = u_data[1:(test_size-1)]
    u_train = u_data[test_size:]

    l_test = l_data[1:(test_size-1)]
    l_train = l_data[test_size:]

    test_data = l_test + u_test
    random.shuffle(test_data)

    train_data = l_train + u_train
    random.shuffle(train_data)

    return train_data, test_data


def output_vec(ltr):
    out = np.zeros((52, 1))
    if ord('A') <= ord(ltr) <= ord('Z'):
        out[ord(ltr) - ord('A')] = 1.0
        return out
    elif ord('a') <= ord(ltr) <= ord('z'):
        ind_out = 26 + (ord(ltr) - ord('a'))
        out[ind_out] = 1.0
        return out


# loading wrapper for extracted (real) data
def extracted_load(extracted_data):

    return [(np.resize(im, (784, 1)), crd) for im, crd in extracted_data]
