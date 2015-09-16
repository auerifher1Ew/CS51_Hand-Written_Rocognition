
import numpy as np
from PIL import Image
import struct

def convert (filename):
	
	img = Image.open(filename)

	#convert to grayscale (bytes 0 - 255)
	grayscl = img.convert('L')

	#get list of all pixel values
	#lst = list(grayscl.getdata())

	#make array of type bytes
	#pixels = np.asarray(lst, dtype = "uint8")
	
	#get darkest values on the page in order to change pixels to either black (0 bytes) or white (255 bytes)
	pixels = list(grayscl.getdata())
	darkest = min(pixels)
	
	#if within 50 pixels of darkest value on page then consider pixel part of letter and set it to black otherwise make it white
	for i in range(len(pixels)):
		if pixels[i] < (darkest + 100):
			pixels[i] = 0
		else:
			pixels[i] = 255

	#pixels = np.asarray(pixels, dtype = "uint8")
	#pixels = struct.pack('i'*len(pixels), *pixels)
	#img = Image.frombuffer('L', img.size, 'raw', pixels, 'L', 0, 1)
	newimg = Image.new('L', img.size)
	newimg.putdata(pixels)
	
	# sudo apt-get install imagemagick
	#newimg.show()
	return newimg
#im=Image.open("test.png")
#convert("notes.jpg")


