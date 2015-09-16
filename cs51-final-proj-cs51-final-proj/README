Handwriting Recognition Tool
============================

To run:

# python gui.py

You must have access to the following libraries:

- Tkinter
- PIL
- numpy
- scipy
- cPickle
- json

From here, you can import image files to be read by the 
recognition network by name, and export the resulting text 
into a .txt file of your choice.


### Recognition.py and Data.py

To run/train/test parameters on the neural network: 

You must have access to the following libraries: 

-random
-numpy
-json
-sys

To train a neural network with various parameters: 

-Create an instace of the Recognition Class with 
Recognition.Recognition([a,b,c], cost=CrossEntropyCost | 
cost=QuadCost) where a is the number of neurons in the 
input layer, b is the number in the middle layer, and c is 
the number in the output layer. The optional agrument 
allows you to choose the type of cost function used
to define the cost in the network. Cross Entropy Proves
more useful in preventing saturation for prolonged 
learning. 

Load testing and training data with the Data module: 

- useing the Data.alpha_load() method, you will be given a 
training and testing set of data, with the ratio (
currently set to 4:1) defined in the Data module.

Train the data set: 

- Set the network to train with net.train(train_set, 
number of runs, size of training samples, training parameter, optional test_data set, optional lambda 
parameter for stbalizing the learning rate) 

- if given testing data, the set set with print the 
accuracy of the network's classification after every round. 

To load data from the extraction module: 

-use the Data.load_extracted(extracted_data) to run the data through our network and return a string of the result. 

To save and load premade networks: 

-simply use the Recognition.load('networkname.json') to 
return a saved network, and (recog_object).save('savename')
to store a network for future use/testing as a json object. 


