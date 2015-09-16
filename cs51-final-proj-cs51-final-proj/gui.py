# this is the GUI! :)

from Tkinter import *
import PIL
import ttk
import Recognition
import extraction3


# displays image at path
def preview():
  image = PhotoImage(file=imPath.get())
  image_display['image'] = image
  
def convert(*args):
  # call extraction functions on the image, return output
  im = PIL.Image.open(imPath.get())
  extracts = extraction3.main3(im)
  net = Recognition.load('network_improved4.json')
  output_string = net.recognize(extracts)

  t.set(output_string)
  ttk.Label(mainframe, textvariable=t).grid(column=4, row=3)

# saves the string into a text file
def export():

  f = open(fileName.get(), W)
  f.write(t.get())
  f.close()

# returns the image path entered
def getImagePath():
  return imPath.get()


root = Tk()
root.title("Handwriting Recognition Tool")



# creates main frame of gui
mainframe = ttk.Frame(root, padding = "30 30 30 30", height = "200", width = "300")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))

# defines the important variables
imPath = StringVar()
fileName = StringVar()
t = StringVar()

# creates the entry field for the image path
imPath_entry = ttk.Entry(mainframe, width=10, textvariable=imPath)
imPath_entry.insert(0, 'FILENAME.png')
imPath_entry.grid(column=1, row=2)

# creates the entry field for the filename
fileName_entry = ttk.Entry(mainframe, width=10, textvariable=fileName)
fileName_entry.insert(0, 'FILENAME')
fileName_entry.grid(column=4, row=4)

# creates the necessary buttons and labels
ttk.Button(mainframe, text="Export Text", command=export).grid(column=4, row=5, sticky=W)
ttk.Button(mainframe, text="Convert", command=convert).grid(column=2, row=3, sticky=W)
ttk.Button(mainframe, text="Preview Image", command=preview).grid(column=2, row=2, sticky=W)
ttk.Label(mainframe, textvariable=imPath).grid(column=1, row=5, sticky=(W, E))
ttk.Label(mainframe, text="Provide Image Path:").grid(column=1, row=1, sticky=(W,E))
ttk.Label(mainframe, text="Text Output").grid(column=4, row=1, sticky=(W,E))

# inserts a blank image placeholder
image = PhotoImage(file='blank.gif')
image_display = ttk.Label(mainframe, image=image)
image_display.grid(column=1, row=3)


# adds padding
for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

# starts cursor at the image path entry 
imPath_entry.focus()
root.bind('<Return>', convert)

root.mainloop()

