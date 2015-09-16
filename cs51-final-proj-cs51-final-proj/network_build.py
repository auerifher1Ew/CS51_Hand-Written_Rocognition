# script for making a saving a neural network
import Recognition
import Data

# get the data
train_data, test_data = Data.alpha_load()

net = Recognition.Recognition([784, 20, 52],
                              cost=Recognition.CrossEntropyCost)

net.train(train_data, 10, 75, 0.1, reg_param=5.0, test_data=test_data)

print net.results(test_data)

net.save('net_smaller.json')

print "Network Saved"
