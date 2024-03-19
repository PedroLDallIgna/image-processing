import tkinter as tk
from tkinter import ttk, filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Processamento de Imagem")
frame = ttk.Frame(root, padding=10)
frame.grid()
img1_label = ttk.Label(frame, text="Imagem a ser selecionada") # label for selected image
img1_label.grid(column=0, row=0, padx=20, pady=20)
img2_label = ttk.Label(frame, text="Imagem transformada") # label for transformed image
img2_label.grid(column=1, row=0, padx=20, pady=20)

# open dialog to select file
def openfilename() -> str:
    # allowed filetypes
    filetypes = (
        ('JPEG', '*.jpg *.jpeg'),
        ('PNG', '*.png'),
        ('TIFF', '*.tiff'),
        ('All files', '*.*')
    )
    
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='./',
        filetypes=filetypes)

    return filename

# negative transformation
def to_negative(image: list) -> list:
    aux = []
    for i in range(len(image)): # iterate over a the flattened array
        pixel = []
        for j in image[i]:
            pixel.append(255 - j) # append the 'negative' pixel
        aux.append(tuple(pixel)) # append to the aux array a tuple of the 'negated' colors
    
    return aux
        
# action for button; gets image by filename and show
def select_image():
    filename = openfilename()

    image = Image.open(filename) # open image with pillow    
    pixels = list(image.getdata()) # gets pixel data of the image

    image2 = Image.new(image.mode, image.size) # creates a new image
    image2.putdata(to_negative(pixels)) # puts the 'negated' data of image

    # shows image in the label
    tkimage1 = ImageTk.PhotoImage(image)
    img1_label.config(image=tkimage1)
    img1_label.image = tkimage1
    
    # shows image2 in the label
    tkimage2 = ImageTk.PhotoImage(image2)
    img2_label.config(image=tkimage2)
    img2_label.image = tkimage2
    

def main():
    open_button = ttk.Button(frame, text="Abrir imagem", command=select_image)
    open_button.grid(column=0, row=1, columnspan=2)
    
    root.mainloop()

if __name__ == "__main__":
    main()
