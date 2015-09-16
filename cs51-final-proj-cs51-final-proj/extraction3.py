from PIL import Image
import cPickle
import numpy as np
import formatting as fm


def sumlist(sumList,store,my_list,width):
    # calculate a sum of pixels along rows
    # the first element of my_list is row number
    # the second element of my_list is the sum of pixels
    for i in range(0,len(my_list)):
        for j in range(0,len(my_list[i])):
            if len(my_list[i])==1:
                my_list[i][j]=my_list[i][0]
            else:
                if j==0:
                    my_list[i][j]=my_list[i][0]
                else:
                    my_list[i][j]=my_list[i][j]+my_list[i][j-1]
    
    # initialzie the sumList
    for i in range(len(my_list)):
        sumList.append(1)
    # get the last element of my_list which is the sum of pixels
    for i in range(0,len(my_list)):
        sumList[i]=my_list[i][len(my_list[i])-1]
    # length of sumList is the same as width
    # white pixels has (255,255,255), so if a column is completely white, it sums up to [width*255, width*255, width*255,width*255]
    # or [width*255, width*255, width*255].
    # [width*255, width*255, width*255,width*255] or [width*255, width*255, width*255] depends on a file. the fourth column is transparency.
    # some fils have this column and some do not have
    for i in range(0,len(sumList)):
        if(len(sumList[0])==4):
            if (sumList[i]==[width*255, width*255, width*255,width*255]).all():
                store.append(i)
                i=i+1
        if(len(sumList[0])==3):
            if (sumList[i]==[width*255, width*255,width*255]).all():
                store.append(i)
                i=i+1

def appending(store,lst1,lst2,height,width):
    # make a list of values to indicate where to crop
    for i in range(0,len(store)-1):
        if not ((store[i]+1)==store[i+1]):
            lst1.append(store[i])
            lst2.append(store[i+1])
    
    if not store[len(store)-1]==width:
        lst1.append(store[len(store)-1])
        lst2.append(height)


def runExtr(image):

    im = image
    # create a list of pixels
    pixels = list(im.getdata())
    # make an array of pixels
    pixels = np.asarray(pixels)
    width, height = im.size
    # initilize 2d array of pixels
    pixels2 = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
    
    my_list=pixels2
    sumList=[]
    store=[]
    #sum up the pixels of each row to see whether each row is completely white or not
    sumlist(sumList,store,my_list,width)
    #cropsstores1 and cropstore2 are arrays to contain where the white from the black occurs in columns
    cropstore1=[]
    cropstore2=[]
    # make a list of values to indicate where to crop by seeing where the change from black to white occurs
    appending(store,cropstore1,cropstore2,height,width)
    
    
    #repeat the same thing by rotating a file
    imrotate=im.rotate(90)
    
    pixels4 = list(imrotate.getdata())
    pixels4 = np.asarray(pixels4)
    width, height = imrotate.size
    pixels3 = [pixels4[i * width:(i + 1) * width] for i in xrange(height)]
    
    sumList=[]
    
    my_list=pixels3
    store=[]
    #sum up the pixels of each row to see whether each row is completely white or not
    sumlist(sumList,store,my_list,width)
    #cropsstores3 and cropstore4 are arrays to contain where the white from the black occurs
    cropstore3=[]
    cropstore4=[]
    # make a list of values to indicate where to crop by seeing where the change from black to white occurs in rows
    appending(store,cropstore3,cropstore4,height,width)
    
    width, height = im.size
    
    img2=[]
    # reverse the order of cropstore3 and cropstore4 in order to get images in correct order
    cropstore4= cropstore4[::-1]
    cropstore3= cropstore3[::-1]
    #crop images based on cropstore values
    for j in range(0,len(cropstore2)):
        for i in range(0,len(cropstore3)):
            aoi = ((width-cropstore4[i]), cropstore1[j], (width-cropstore3[i]) , cropstore2[j])
            img2.append(im.crop(aoi))
    
    img6=[]
    
    #Now look at individual file and remove white space
    for g in range(0,len(img2)):
        #repeat the same process as above by rotating the file by 90 degrees
        im=img2[g].rotate(90)
        
        pixels5 = list(im.getdata())
        pixels5 = np.asarray(pixels5)
        width, height = im.size
        
        pixels6 = [pixels5[i * width:(i + 1) * width] for i in xrange(height)]
        
        sumList=[]
        
        my_list=[]
        my_list=pixels6
        
        store=[]
        sumlist(sumList,store,my_list,width)
        
        cropstore3=[]
        cropstore4=[]
        appending(store,cropstore3,cropstore4,height,width)
        
        im=img2[g]
        
        img4=[]
        aoi=[]
        
        width, height = im.size
        
        for i in range(0,len(cropstore3)):
            aoi.append(((width-cropstore4[i]), 0, (width-cropstore3[i]) , height))
            img4.append(im.crop(aoi[i]))
        
        im=img4[0]
        
        #reverse the order of img4 by reversing the order
        img4=img4[::-1]
        #repeat the same process as above for all the images
        for numb in range(0,len(img4)):
            im=img4[numb]
            pixels7 = list(im.getdata())
            pixels7 = np.asarray(pixels7)
            width, height = im.size
            
            pixels8 = [pixels7[i * width:(i + 1) * width] for i in xrange(height)]
            
            sumList=[]
            
            my_list=[]
            my_list=pixels8
            
            store=[]
            
            sumlist(sumList,store,my_list,width)
            
            cropstore5=[]
            cropstore6=[]
            appending(store,cropstore5,cropstore6,height,width)
            
            
            im=img4[numb]
            aoi2=[]
            
            img5=[]
            width, height = im.size
            
            for p in range(0,len(cropstore5)):
                aoi2.append((0, cropstore5[p], width ,cropstore6[p]))
                img5.append(im.crop(aoi2[p]))
            if not img5[0].size==(1,1):
                img6.append(img5[0])
    
    img7=[]
    for i in range(0,len(img6)):
        img7.append(1)
    #change the size of pixel image into 28 by 28 in order to recognize correctly
    for p in range(0,len(img6)):
        img7[p] = img6[p].resize((28, 28), Image.ANTIALIAS)
    output2=[]
    for j in range(0,len(img7)):
        pixels=[]
        pixels = list(img7[j].getdata())
        # make an array of pixels
        pixels = np.asarray(pixels)
        
        numpyarray=[]
        #make a numpyarray of 0 and 1 to indicate whether the pixel is white or other color
        #if white 1 and if other color 0
        for n in range(0,len(pixels)):
            if(len(pixels[n])==4):
                if (pixels[n]==[255, 255, 255,255]).all():
                    numpyarray.append(1.)
                else:
                    numpyarray.append(0.)
            if(len(pixels[n])==3):
                if (pixels[n]==[255, 255, 255]).all():
                    numpyarray.append(1.)
                else:
                    numpyarray.append(0.)
        numpyarray=np.asarray(numpyarray)
        output2.append(numpyarray)

    return output2

def main2(im):
    
    #repeat the same thing by rotating a file
    imrotate=im.rotate(90)
    
    pixels4 = list(imrotate.getdata())
    pixels4 = np.asarray(pixels4)
    width, height = imrotate.size
    pixels3 = [pixels4[i * width:(i + 1) * width] for i in xrange(height)]
    
    sumList=[]
    
    my_list=pixels3
    store=[]
    #sum up the pixels of each row to see whether each row is completely white or not
    sumlist(sumList,store,my_list,width)
    #cropsstores3 and cropstore4 are arrays to contain where the white from the black occurs
    cropstore3=[]
    cropstore4=[]
    # make a list of values to indicate where to crop by seeing where the change from black to white occurs in rows
    appending(store,cropstore3,cropstore4,height,width)

    if cropstore4[len(cropstore4)-1]==height:
        del cropstore4[-1]
        del cropstore3[-1]
        
    # create a list of pixels
    pixels = list(im.getdata())
    # make an array of pixels
    pixels = np.asarray(pixels)
    width, height = im.size
    # initilize 2d array of pixels
    pixels2 = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
    
    my_list=pixels2
    sumList=[]
    store=[]
    #sum up the pixels of each row to see whether each row is completely white or not
    sumlist(sumList,store,my_list,width)
    #cropsstores1 and cropstore2 are arrays to contain where the white from the black occurs in columns
    cropstore1=[]
    cropstore2=[]
    aoi=[]
    # make a list of values to indicate where to crop by seeing where the change from black to white occurs
    appending(store,cropstore1,cropstore2,height,width)

    for g in range(0,len(cropstore2)):
        aoi.append((0, cropstore1[g], width, cropstore2[g]))
    
    im2=[]
    for p in range(0,len(aoi)-1):
        im2.append(im.crop(aoi[p]))

    storing = []

    for p in range(0,len(im2)):
        im=im2[p]
        imrotate=im.rotate(90)
        
        pixels4 = list(imrotate.getdata())
        pixels4 = np.asarray(pixels4)
        width, height = imrotate.size
        pixels3 = [pixels4[i * width:(i + 1) * width] for i in xrange(height)]
        
        sumList=[]
        
        my_list=pixels3
        store=[]
        #sum up the pixels of each row to see whether each row is completely white or not
        sumlist(sumList,store,my_list,width)
        #cropsstores3 and cropstore4 are arrays to contain where the white from the black occurs
        cropstore3=[]
        cropstore4=[]
        # make a list of values to indicate where to crop by seeing where the change from black to white occurs in rows
        appending(store,cropstore3,cropstore4,height,width)



        cropstore4= cropstore4[::-1]
        cropstore3= cropstore3[::-1]

        mean=[]
        if not len(cropstore4)==0:
            for h in range(0,len(cropstore3)-1):
                mean.append(cropstore3[h]-cropstore4[h+1])
        whitespace= sum(mean)/len(mean)
        #if whitespace is bigger than the mean of white spaces between lettters, we think that there is space between letters
        #if there is white space before a char, give that char a value of 1 and store into storing as (row,1) 
        #if there is no white space before a char, give that char a value of 0 and store into storing as (row,0) 
        if not len(cropstore4)==0:
            for h in range(0,len(cropstore3)-1):
                if cropstore3[h]-cropstore4[h+1]<whitespace:
                    storing.append((p,1))
                else:

                    storing.append((p,0))
    
    return storing
def main3(im):
    result1=runExtr(im)
    result2=main2(im)
    zipped = zip(result1, result2)
    return zipped