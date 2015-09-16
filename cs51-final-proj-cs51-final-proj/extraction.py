# this file will contain processes to extract individual characters from an 
# image that contains what we would interpret as text

# look at image as a 2-dimensional array, provided by formatting.py

# get the height and width of the image 
from PIL import Image
im=Image.open(filepath)
im.size
# look at the first pixel

# create an array of labels to correspond to each pixelx
labels[width][height] = {}

current_color = # pick up the color value of the pixel as an integer

# two pass algorithm
label()
# Does the pixel to the left (West) have the same value as the current pixel?
# Yes – We are in the same region. Assign the same label to the current pixel
# No – Check next condition
# Do both pixels to the North and West of the current pixel have the same value as the current pixel but not the same label?
# Yes – We know that the North and West pixels belong to the same region and must be merged. Assign 
#the current pixel the minimum of the North and West labels, and record their equivalence relationship
# No – Check next condition
# Does the pixel to the left (West) have a different value and the one to the North the same value as the current pixel?
# Yes – Assign the label of the North pixel to the current pixel
# No – Check next condition

# Do the pixel's North and West neighbors have different pixel values than current pixel?
# Yes – Create a new label id and assign it to the current pixel

# do this for every pixel

# returns the minimum label value that is equivalent to the function argument 'l'.
findSet(l) 

# Once the initial labeling and equivalence recording is completed, the second pass merely replaces each pixel label 
# with its equivalent disjoint-set representative element.

# scale the object so that it can be interpretted later
scale(imagearray)

# returns the array of each image piece
getObject()

