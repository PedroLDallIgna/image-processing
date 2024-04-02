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
        self.buttons_frame = ttk.Frame(self.frame, padding=5)

        self.input_img_label = ttk.Label(self.frame, text="Imagem de entrada", width="40", anchor=CENTER) # label for selected image
        self.input_img = None
        self.input_img2_label = ttk.Label(self.frame, text="Imagem de entrada 2", width="40", anchor=CENTER) # label for selected image
        self.input_img2 = None
        self.output_img_label = ttk.Label(self.frame, text="Imagem de saída", width="40", anchor=CENTER) # label for transformed image
        self.output_img = None

        self.save_button = ttk.Button(self.frame, text="Salvar imagem", command=self._save_image, width="27")
        self.open_button = ttk.Button(self.frame, text="Abrir imagem", command=self._select_image_1, width="27")
        self.reset_button = ttk.Button(self.frame, text="Descartar tudo", command=self._reset, width="27")
        
        self.open_button2 = ttk.Button(self.buttons_frame, text="Abrir nova imagem", command=self._select_image_2, width="27")
        self.flip_vertically_button = ttk.Button(self.buttons_frame, text="Inverter verticalmente", command=self._flip_vertically, width="27")
        self.flip_horizontally_button = ttk.Button(self.buttons_frame, text="Inverter horizontalmente", command=self._flip_horizontally, width="27")
        self.grayscale_button = ttk.Button(self.buttons_frame, text="Escala de cinza", command=self._to_grayscale, width="27")
        self.negative_button = ttk.Button(self.buttons_frame, text="Negativo", command=self._to_negative, width="27")
        self.sum_images_button = ttk.Button(self.buttons_frame, text="Somar imagens", command=self._sum_images, width="27")
        self.subt_images_button = ttk.Button(self.buttons_frame, text="Subtrair imagens", command=self._subt_images, width="27")
        self.limiarize_button = ttk.Button(self.buttons_frame, text="Limiarizar", command=self._limiarize, width="27")

    def _config(self) -> None:
        self.root.title("Processamento de Imagem")
        self.frame.grid()
        self.buttons_frame.grid(column=2, row=0)
        self.input_img_label.grid(column=0, row=0, padx=20, pady=20)
        self.output_img_label.grid(column=3, row=0, padx=20, pady=20)
        self.open_button.grid(column=0, row=1)

    def run(self) -> None:
        self._config()
        self.root.mainloop()

    def _select_image_1(self) -> None:
        """Action of the open button"""
        try:
            filename = self._openfilename()
            
            self.input_img = Image.open(filename) # open image with pillow    
            self.open_button.config(text="Trocar Imagem")

            input_img_data = list(self.input_img.getdata()) # gets pixel data of the input image

            self.output_img = Image.new(self.input_img.mode, self.input_img.size) # creates a new image
            self.output_img.putdata(input_img_data) # puts the input image data (copy)
        
            # shows input image in the label
            self._show_image(self.input_img, self.input_img_label)
            
            # shows output image in the label
            self._show_image(self.output_img, self.output_img_label)

            # show the action buttons
            self.open_button2.grid(column=0, row=0)
            self.flip_vertically_button.grid(column=0, row=1)
            self.flip_horizontally_button.grid(column=0, row=2)
            self.grayscale_button.grid(column=0, row=3)
            self.negative_button.grid(column=0, row=4)
            self.save_button.grid(column=3, row=1)
            self.reset_button.grid(column=3, row=2)

        except:
            print("imagem não selecionada")

    def _select_image_2(self) -> None:
        """Action of the open button"""
        try:
            filename = self._openfilename()
            
            self.input_img2 = Image.open(filename) # open image with pillow    
            self.open_button2.config(text="Trocar Imagem")

            self.input_img2_label.grid(column=1, row=0, padx=20, pady=20)
        
            # shows input image in the label
            self._show_image(self.input_img2, self.input_img2_label)

            self.sum_images_button.grid(column=0, row=5)
            self.subt_images_button.grid(column=0, row=6)

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
        image = self.output_img
        image_data = list(image.getdata())
        negative_image = []
        for i in range(len(image_data)): # iterate over a the flattened array
            negative_pixel = []
            for j in image_data[i]:
                negative_pixel.append(255 - j) # append the 'negative' pixel
            negative_image.append(tuple(negative_pixel)) # append to the aux array a tuple of the 'negated' colors
        
        self.output_img.putdata(negative_image)

        self._show_image(self.output_img, self.output_img_label)

    def _to_grayscale(self):
        """Convert the an image to grayscale"""
        image = self.output_img
        image_data = list(image.getdata())
        grayscale_img_data = []

        for pixel in image_data:
            new_pixel = (pixel[0] + pixel[1] + pixel[2]) / 3
            grayscale_img_data.append(new_pixel)

        grayscale_img = Image.new('L', image.size)
        grayscale_img.putdata(grayscale_img_data)

        self.output_img = grayscale_img
        self._show_image(self.output_img, self.output_img_label)

        self.limiarize_button.grid(column=0, row=7)

    def _reset(self) -> None:
        """Reset the transformed image to base"""
        if (self.output_img.mode != self.input_img.mode):
            self.output_img = self.output_img.convert(self.input_img.mode)

        self.output_img.putdata(self.input_img.getdata())
        
        self._show_image(self.output_img, self.output_img_label)

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
        """Transforms the flat image data list (unidimensional) into an unflat (bidimensinal) image data list"""
        unflattened_data = []
        for row in range(height):
            unflattened_data.append(flattened_data[row*width:(row+1)*width])

        return unflattened_data

    def _flat_data(self, unflattened_data):
        """Transforms the unflat image data list (bidimensional) into a flat (unidimensional) image data list"""
        flattened_data = []
        for row in unflattened_data:
            flattened_data += row

        return flattened_data

    def _flip_vertically(self):
        """Vertically flips the image"""
        image = self.output_img
        img_data = self._unflat_data(list(image.getdata()), image.height, image.width)
        flipped_img = Image.new(image.mode, image.size)
        flipped_img_data = []
        for row in range(len(img_data) - 1, -1, -1):
            flipped_img_data.append(img_data[row])

        flipped_img.putdata(self._flat_data(flipped_img_data))
        self.output_img = flipped_img

        self._show_image(self.output_img, self.output_img_label)

    def _flip_horizontally(self):
        """Horizontally flips the image"""
        image = self.output_img
        img_data = self._unflat_data(list(image.getdata()), image.height, image.width)
        flipped_img = Image.new(image.mode, image.size)
        flipped_img_data = []
        for row in range(len(img_data)):
            flipped_row = []
            for col in range(len(img_data[row]) - 1, -1, -1):
                flipped_row.append(img_data[row][col])
            flipped_img_data.append(flipped_row)

        flipped_img.putdata(self._flat_data(flipped_img_data))
        self.output_img = flipped_img

        self._show_image(self.output_img, self.output_img_label)
    

    def _show_image(self, image, image_label):
        """Shows the given image in the given label reescaling it"""
        tkimage = ImageTk.PhotoImage(self._scale_image_label(image))
        image_label.config(image=tkimage)
        image_label.image = tkimage


    def _scale_image_label(self, image, base_width=300):
        """Reescales an image based on base_width"""
        wpercent = (base_width / float(image.width))
        hsize = int((float(image.height) * float(wpercent)))

        return image.resize((base_width, hsize), Image.Resampling.LANCZOS)


    def _sum_images(self):
        """Sum the two input images and shows as output image"""
        img1 = self.input_img
        img2 = self.input_img2

        if (img1.width != img2.width or img1.height != img2.height):
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)

        img1_data = list(img1.getdata())
        img2_data = list(img2.getdata())

        out_img = []
        for pixel in range(len(img1_data)):
            new_pixel = []
            for color in range(len(img1_data[pixel])):
                new_pixel_color = img1_data[pixel][color] + img2_data[pixel][color]
                if new_pixel_color > 255:
                    new_pixel.append(255)
                else:
                    new_pixel.append(new_pixel_color)
            out_img.append(tuple(new_pixel))

        self.output_img.putdata(out_img)

        self._show_image(self.output_img, self.output_img_label)

    def _subt_images(self):
        """Subtract the two input images and shows as output image"""
        img1 = self.input_img
        img2 = self.input_img2

        if (img1.width != img2.width or img1.height != img2.height):
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)

        img1_data = list(img1.getdata())
        img2_data = list(img2.getdata())

        out_img = []
        for pixel in range(len(img1_data)):
            new_pixel = []
            for color in range(len(img1_data[pixel])):
                new_pixel_color = img1_data[pixel][color] - img2_data[pixel][color]
                if new_pixel_color < 0:
                    new_pixel.append(0)
                else:
                    new_pixel.append(new_pixel_color)
            out_img.append(tuple(new_pixel))

        self.output_img.putdata(out_img)

        self._show_image(self.output_img, self.output_img_label)

    def _limiarize(self):
        """Limiarize an image"""
        image = self.output_img
        img_data = list(image.getdata())
        binary_img_data = []

        for pixel in img_data:
            new_pixel = 0 if pixel <= 128 else 255
            binary_img_data.append(new_pixel)

        binary_img = Image.new('1', image.size)
        binary_img.putdata(binary_img_data)

        self.output_img = binary_img
        self._show_image(self.output_img, self.output_img_label)


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
