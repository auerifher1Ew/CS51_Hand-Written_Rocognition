# script for making a saving a neural network
import Recognition
import Data

# get the data
train_data, test_data = Data.alpha_load()

net = Recognition.load('network_improved3.json')

net.train(train_data, 5, 104, 0.1, reg_param=5.0, test_data=test_data)

net.save('network_improved4.json')

print "Network Saved"
