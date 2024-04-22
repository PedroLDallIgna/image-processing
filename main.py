import tkinter as tk
from tkinter import ttk, filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.constants import *
from PIL import Image, ImageTk
import process

class MainApplication():
    """Application to upload an image and make transformations"""

    def __init__(self):
        self.root = tk.Tk()
        self.frame = ttk.Frame(self.root, padding=10)
        self.buttons_frame = ttk.Frame(self.frame, padding=5)
        self.binary_btns_frame = ttk.Frame(self.buttons_frame)

        self.input_img_label = ttk.Label(self.frame, text="Imagem de entrada", width="40", anchor=CENTER) # label for selected image
        self.input_img = None
        self.input_img2_label = ttk.Label(self.frame, text="Imagem de entrada 2", width="40", anchor=CENTER) # label for selected image
        self.input_img2 = None
        self.output_img_label = ttk.Label(self.frame, text="Imagem de saída", width="40", anchor=CENTER) # label for transformed image
        self.output_img = None

        self.save_button = ttk.Button(self.frame, text="Salvar imagem", command=self._save_image, width="27")
        self.open_button = ttk.Button(self.frame, text="Abrir imagem", command=self._select_image_1, width="27")
        self.reset_button = ttk.Button(self.frame, text="Descartar tudo", command=self._reset, width="27")
        self.open_button2 = ttk.Button(self.buttons_frame, text="Abrir nova imagem", command=self._select_image_2)
        self.change_img2_button = ttk.Button(self.frame, text="Trocar imagem", command=self._select_image_2, width="27")
        self.remove_img2_button = ttk.Button(self.frame, text="Remover imagem", command=self._remove_image_2, width="27")
        
        self.flip_vertically_button = ttk.Button(self.buttons_frame, text="Inverter verticalmente", command=self._flip_vertically, width="27")
        self.flip_horizontally_button = ttk.Button(self.buttons_frame, text="Inverter horizontalmente", command=self._flip_horizontally, width="27")
        self.grayscale_button = ttk.Button(self.buttons_frame, text="Escala de cinza", command=self._to_grayscale, width="27")
        self.negative_button = ttk.Button(self.buttons_frame, text="Negativo", command=self._to_negative, width="27")
        self.sum_images_button = ttk.Button(self.buttons_frame, text="Somar imagens", command=self._sum_images, width="27")
        self.subt_images_button = ttk.Button(self.buttons_frame, text="Subtrair imagens", command=self._subt_images, width="27")
        self.limiar_value = tk.IntVar()
        self.limiar_entry = ttk.Entry(self.buttons_frame, textvariable=self.limiar_value, width="27")
        self.limiarize_button = ttk.Button(self.buttons_frame, text="Limiarizar", command=self._limiarize, width="27")
        self.histogram_button = ttk.Button(self.buttons_frame, text="Eq. Histograma", command=self._equalize_histogram, width="27")
        self.concat_button = ttk.Button(self.buttons_frame, text="Concatenar", command=self._concat_images, width="27")

        self.brightness_value = tk.IntVar()
        self.brightness_value.set(0)
        self.brightness_label = ttk.Label(self.buttons_frame, text=f"Brilho: {int(self.brightness_value.get())}%", width=27, anchor='w')
        self.brightness_slider = ttk.Scale(self.buttons_frame, from_=-100, to=100, orient='horizontal', variable=self.brightness_value)
        self.brightness_slider.bind("<ButtonRelease-1>", self._brightness)
        self.brightness_slider.bind("<Button1-Motion>", lambda event: self.brightness_label.config(text=f"Brilho: {int(self.brightness_value.get())}%"))

        self.contrast_value = tk.IntVar()
        self.contrast_value.set(0)
        self.contrast_label = ttk.Label(self.buttons_frame, text=f"Contraste: {int(self.contrast_value.get())}%", width=27, anchor='w')
        self.contrast_slider = ttk.Scale(self.buttons_frame, from_=-100, to=100, orient='horizontal', variable=self.contrast_value)
        self.contrast_slider.bind("<ButtonRelease-1>", self._contrast)
        self.contrast_slider.bind("<Button1-Motion>", lambda event: self.contrast_label.config(text=f"Contraste: {int(self.contrast_value.get())}%"))

        self.blending_value = tk.IntVar()
        self.blending_value.set(50)
        self.blending_label = ttk.Label(self.buttons_frame, text=f"Blending: {int(self.blending_value.get())}%", width=27, anchor='w')
        self.blending_slider = ttk.Scale(self.buttons_frame, from_=0, to=100, orient='horizontal', variable=self.blending_value)
        self.blending_slider.bind("<ButtonRelease-1>", self._blending)
        self.blending_slider.bind("<Button1-Motion>", lambda event: self.blending_label.config(text=f"Blending: {int(self.blending_value.get())}%"))

        self.not_button = ttk.Button(self.binary_btns_frame, text="NOT", command=self._negate)
        self.and_button = ttk.Button(self.binary_btns_frame, text="AND", command=self._and)
        self.or_button = ttk.Button(self.binary_btns_frame, text="OR", command=self._or)

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

            self.output_img = self.input_img.copy()

            # shows input image in the label
            self._show_image(self.input_img, self.input_img_label)
            
            # shows output image in the label
            self._show_image(self.output_img, self.output_img_label)

            # show the action buttons
            self.open_button2.grid(column=0, sticky='we')
            self.flip_vertically_button.grid(column=0)
            self.flip_horizontally_button.grid(column=0)
            self.grayscale_button.grid(column=0)
            self.negative_button.grid(column=0)
            self.histogram_button.grid(column=0)
            self.brightness_label.grid(column=0)
            self.brightness_slider.grid(column=0, sticky="we")
            self.contrast_label.grid(column=0)
            self.contrast_slider.grid(column=0, sticky="we")
            self.save_button.grid(column=3, row=1)
            self.reset_button.grid(column=3, row=2)

            self.binary_btns_frame.grid(column=0, row=20, sticky='we')
            self.not_button.grid(column=0, row=0)
            self.and_button.grid(column=1, row=0)
            self.or_button.grid(column=2, row=0)


        except:
            print("imagem não selecionada")

    def _select_image_2(self) -> None:
        """Action of the open button"""
        try:
            filename = self._openfilename()
            
            self.input_img2 = Image.open(filename) # open image with pillow    
            self.open_button2.grid_remove()

            self.input_img2_label.grid(column=1, row=0, padx=20, pady=20)
        
            # shows input image in the label
            self._show_image(self.input_img2, self.input_img2_label)

            self.change_img2_button.grid(column=1, row=1)
            self.remove_img2_button.grid(column=1, row=2)
            self.sum_images_button.grid(column=0)
            self.subt_images_button.grid(column=0)
            self.concat_button.grid(column=0)
            self.blending_label.grid(column=0)
            self.blending_slider.grid(column=0, sticky='we')

        except:
            print("imagem não selecionada")

    def _openfilename(self) -> str:
        """Open dialog to select a file and returns the path"""
        # allowed filetypes
        filetypes = (
            ('All files', '*.*'),
            ('JPEG', '*.jpg *.jpeg'),
            ('PNG', '*.png'),
            ('TIFF', '*.tiff')
        )
        
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./',
            filetypes=filetypes)

        return filename

    def _remove_image_2(self):
        self.input_img2 = None
        self.input_img2_label.grid_remove()
        self.change_img2_button.grid_remove()
        self.remove_img2_button.grid_remove()
        self.open_button2.grid(column=0, row=0)

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
        """Convert the input image to grayscale"""

        grayscale_img = None

        if (self.input_img.mode != 'L'):
            image = self.input_img
            # image_data = list(image.getdata())
            grayscale_img_data = process.to_grayscale(image)

            grayscale_img = Image.new('L', image.size)
            grayscale_img.putdata(grayscale_img_data)

        else:
            grayscale_img = self.input_img.copy()

        self.output_img = grayscale_img
        
        self._show_image(self.output_img, self.output_img_label)

        self.limiar_entry.grid(column=0)
        self.limiarize_button.grid(column=0)


    def _reset(self) -> None:
        """Reset the transformed image to base"""
        if (self.output_img.mode != self.input_img.mode):
            self.output_img = self.output_img.convert(self.input_img.mode)

        reseted_img = self.input_img.copy()
        self.output_img = reseted_img
        
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

        try:
            out_img = process.sum_images(img1, img2)

            self.output_img.putdata(out_img)

            self._show_image(self.output_img, self.output_img_label)
        except:
            showinfo("Modos de imagem diferentes", "Os modos das imagens são diferentes")
        

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
        
        limiar = self.limiar_value.get()

        for pixel in img_data:
            new_pixel = 0 if pixel <= limiar else 255
            binary_img_data.append(new_pixel)

        binary_img = Image.new('1', image.size)
        binary_img.putdata(binary_img_data)

        self.output_img = binary_img
        self._show_image(self.output_img, self.output_img_label)

    def _equalize_histogram(self):
        im = self.input_img

        out_img_data = process.equalize_histogram(im)
        
        self.output_img.putdata(out_img_data)

        self._show_image(self.output_img, self.output_img_label)

    def _concat_images(self):
        out_img_data = process.concat_images(self.input_img, self.input_img2)
        out_img = Image.new(self.input_img.mode, (self.input_img.width + self.input_img2.width, self.input_img.height))

        out_img.putdata(out_img_data)
        self.output_img = out_img

        self._show_image(self.output_img, self.output_img_label)


    def _brightness(self, event):
        brightness_update = (int(self.brightness_value.get()) * (256 / 100))

        out_img_data = process.change_brightness(self.input_img, brightness_update)

        self.output_img.putdata(out_img_data)

        self._show_image(self.output_img, self.output_img_label)

    def _contrast(self, event):
        contrast_value = (1 + (self.contrast_value.get() / 100))

        out_img_data = process.change_contrast(self.input_img, contrast_value)

        self.output_img.putdata(out_img_data)

        self._show_image(self.output_img, self.output_img_label)


    def _blending(self, event):
        blending_value = self.blending_value.get() / 100

        out_img_data = process.blend(self.input_img, self.input_img2, blending_value)

        self.output_img.putdata(out_img_data)

        self._show_image(self.output_img, self.output_img_label)

    def _negate(self):
        im = self.input_img
        im_data = None

        if (im.mode != 'L'):
            im_data = process.to_grayscale(im)

            im = Image.new('L', im.size)
            im.putdata(im_data)

        out_im = Image.new('1', im.size)
        out_im_data = process.negate(im)
        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _and(self):
        im1 = self.input_img
        im2 = self.input_img2

        for im in [im1, im2]:
            if (im.mode != 'L'):
                im_data = process.to_grayscale(im)

                im = Image.new('L', im.size)
                im.putdata(im_data)

        for im in [im1, im2]:
            im_data = process.binarize(im)
            im = Image.new('1', im.size)
            im.putdata(im_data)

        out_im = Image.new('1', im1.size)
        out_im_data = process.and_(im1, im2)
        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _or(self):
        im1 = self.input_img
        im2 = self.input_img2

        for im in [im1, im2]:
            if (im.mode != 'L'):
                im_data = process.to_grayscale(im)

                im = Image.new('L', im.size)
                im.putdata(im_data)

        for im in [im1, im2]:
            im_data = process.binarize(im)
            im = Image.new('1', im.size)
            im.putdata(im_data)

        out_im = Image.new('1', im1.size)
        out_im_data = process.or_(im1, im2)
        out_im.putdata(out_im_data)

        self.output_img = out_im

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
