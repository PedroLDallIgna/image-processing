import tkinter as tk
from tkinter import ttk, filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.constants import *
from PIL import Image, ImageTk

class MainApplication():
    """Application to upload an image and make transformations"""

    def __init__(self):
        self.root = tk.Tk()
        self.frame = ttk.Frame(self.root, padding=10)
        self.input_img_label = ttk.Label(self.frame, text="Imagem de entrada") # label for selected image
        self.input_img = None
        self.output_img_label = ttk.Label(self.frame, text="Imagem de saída") # label for transformed image
        self.output_img = None
        self.open_button = ttk.Button(self.frame, text="Abrir imagem", command=self._select_image)
        self.negative_button = ttk.Button(self.frame, text="Negativo", command=self._to_negative)
        self.reset_button = ttk.Button(self.frame, text="Descartar tudo", command=self._reset)
        self.save_button = ttk.Button(self.frame, text="Salvar imagem", command=self._save_image)
        self.flip_vertically_button = ttk.Button(self.frame, text="Inverter verticalmente", command=self._flip_vertically)

    def _config(self) -> None:
        self.root.title("Processamento de Imagem")
        self.frame.grid()
        self.input_img_label.grid(column=0, row=0, padx=20, pady=20)
        self.output_img_label.grid(column=1, row=0, padx=20, pady=20)
        self.open_button.grid(column=0, row=1, columnspan=2)

    def run(self) -> None:
        self._config()
        self.root.mainloop()

    def _select_image(self) -> None:
        """Action of the open button"""
        try:
            filename = self._openfilename()

            self.open_button.config(text="Trocar Imagem")

            self.input_img = Image.open(filename) # open image with pillow    
            pixels = list(self.input_img.getdata()) # gets pixel data of the image

            self.output_img = Image.new(self.input_img.mode, self.input_img.size) # creates a new image
            self.output_img.putdata(pixels) # puts the 'negated' data of image

            # shows image in the label
            tkimage1 = ImageTk.PhotoImage(self.input_img)
            self.input_img_label.config(image=tkimage1)
            self.input_img_label.image = tkimage1
            
            # shows image2 in the label
            tkimage2 = ImageTk.PhotoImage(self.output_img)
            self.output_img_label.config(image=tkimage2)
            self.output_img_label.image = tkimage2

            self.negative_button.grid(column=0, row=2, columnspan=2)
            self.reset_button.grid(column=0, row=3, columnspan=2)
            self.save_button.grid(column=0, row=4, columnspan=2)
            self.flip_vertically_button.grid(column=0, row=5, columnspan=2)

        except:
            print("imagem não selecionada")

    def _openfilename(self) -> str:
        """Open dialog to select a file and returns the path"""
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

    def _to_negative(self) -> None:
        """Convert the base image pixels to negative"""

        image = self.input_img.getdata()
        negative_image = []
        for i in range(len(image)): # iterate over a the flattened array
            negative_pixel = []
            for j in image[i]:
                negative_pixel.append(255 - j) # append the 'negative' pixel
            negative_image.append(tuple(negative_pixel)) # append to the aux array a tuple of the 'negated' colors
        
        self.output_img.putdata(negative_image)
        
        tkimage2 = ImageTk.PhotoImage(self.output_img)
        self.output_img_label.config(image=tkimage2)
        self.output_img_label.image = tkimage2

    def _reset(self) -> None:
        """Reset the transformed image to base"""
        self.output_img.putdata(self.input_img.getdata())
        
        tkimage2 = ImageTk.PhotoImage(self.output_img)
        self.output_img_label.config(image=tkimage2)
        self.output_img_label.image = tkimage2

    def _savefilename(self):
        """Open dialog to select a filename and returns the path"""
        filetypes = (
            ('JPEG', '*.jpg *.jpeg'),
            ('PNG', '*.png'),
            ('TIFF', '*.tiff'),
            ('All files', '*.*')
        )

        filename = fd.asksaveasfilename(
            title='Open a file',
            initialdir='./',
            filetypes=filetypes
        )

        return filename

    def _save_image(self):
        """Action for the save button"""

        filename = self._savefilename()

        self.output_img.save(filename)

    def _unflat_data(self, flattened_data, height, width):
        unflattened_data = []
        for row in range(height):
            unflattened_data.append(flattened_data[row*width:(row+1)*width])

        return unflattened_data

    def _flat_data(self, unflattened_data):
        flattened_data = []
        for row in unflattened_data:
            flattened_data += row

        return flattened_data

    def _flip_vertically(self):
        image = self.input_img
        img_data = self._unflat_data(list(image.getdata()), image.height, image.width)
        flipped_img = Image.new(image.mode, image.size)
        flipped_img_data = []
        for row in range(len(img_data) - 1, -1, -1):
            flipped_img_data.append(img_data[row])
            # for col in range(image.width):
            #     flipped_img_data.append(self.get_pixel(image, row, col))

        flipped_img.putdata(self._flat_data(flipped_img_data))
        self.output_img = flipped_img
        tkimage2 = ImageTk.PhotoImage(self.output_img)
        self.output_img_label.config(image=tkimage2)
        self.output_img_label.image = tkimage2


    def get_pixel(self, image, row, col, depth=None):
        img_data = list(image.getdata())
        rows = image.height
        cols = image.width

        index = row * cols + col

        if (depth != None):
            return img_data[index][depth]
        return img_data[index]

if __name__ == "__main__":
    app = MainApplication()
    app.run()
