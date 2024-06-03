import tkinter as tk
from tkinter import ttk, filedialog as fd
from tkinter.messagebox import showerror, showinfo
from tkinter.constants import *
from PIL import Image, ImageTk
import matplotlib
import process

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApplication():
    """Application to upload an image and make transformations"""

    def __init__(self):
        self.root = tk.Tk()
        self.frame = ttk.Frame(self.root, padding=10)
        self.buttons_frame = ttk.Frame(self.frame, padding=5)

        self.input_img_frame = ttk.Frame(self.frame)
        self.input_img_label = ttk.Label(self.input_img_frame, text="Imagem de entrada", width=40, anchor=CENTER) # label for selected image
        self.input_img = None

        self.input_img2_frame = ttk.Frame(self.frame)
        self.input_img2_label = ttk.Label(self.input_img2_frame, text="Imagem de entrada 2", width=40, anchor=CENTER) # label for selected image
        self.input_img2 = None

        self.output_img_frame = ttk.Frame(self.frame)
        self.output_img_label = ttk.Label(self.output_img_frame, text="Imagem de saída", width=40, anchor=CENTER) # label for transformed image
        self.output_img = None

        self.open_button = ttk.Button(self.input_img_frame, text="Abrir imagem", command=self._select_image_1, width=27)
        self.save_button = ttk.Button(self.output_img_frame, text="Salvar imagem", command=self._save_image, width=27)
        self.reset_button = ttk.Button(self.output_img_frame, text="Descartar tudo", command=self._reset, width=27)
        self.open_button2 = ttk.Button(self.buttons_frame, text="Abrir nova imagem", command=self._select_image_2)
        self.change_img2_button = ttk.Button(self.input_img2_frame, text="Trocar imagem", command=self._select_image_2, width=27)
        self.remove_img2_button = ttk.Button(self.input_img2_frame, text="Remover imagem", command=self._remove_image_2, width=27)

        self.arithmetic_ops_frame = ttk.Labelframe(self.buttons_frame, text='Operações artiméticas')
        self.arithmetic_ops_frame.columnconfigure(0, weight=4)
        self.arithmetic_ops_frame.columnconfigure(1, weight=1)
        self.addition_value = tk.IntVar(value=0)
        self.addition_entry = ttk.Entry(self.arithmetic_ops_frame, textvariable=self.addition_value, width=5, justify='right')
        self.addition_button = ttk.Button(self.arithmetic_ops_frame, text="Adição", command=self._do_arithmetic_op('+'))
        self.subtraction_value = tk.IntVar(value=0)
        self.subtraction_entry = ttk.Entry(self.arithmetic_ops_frame, textvariable=self.subtraction_value, width=5, justify='right')
        self.subtraction_button = ttk.Button(self.arithmetic_ops_frame, text="Subtração", command=self._do_arithmetic_op('-'))
        self.multiplication_value = tk.DoubleVar(value=1.0)
        self.multiplication_entry = ttk.Entry(self.arithmetic_ops_frame, textvariable=self.multiplication_value, width=5, justify='right')
        self.multiplication_button = ttk.Button(self.arithmetic_ops_frame, text="Multiplicação", command=self._do_arithmetic_op('*'))
        self.division_value = tk.DoubleVar(value=1.0)
        self.division_entry = ttk.Entry(self.arithmetic_ops_frame, textvariable=self.division_value, width=5, justify='right')
        self.division_button = ttk.Button(self.arithmetic_ops_frame, text="Divisão", command=self._do_arithmetic_op('/'))

        self.subim_op_frame = ttk.Labelframe(self.buttons_frame, text='Sub-Imagem')
        self.subim_x_start_label = ttk.Label(self.subim_op_frame, text="Início(x)")
        self.subim_x_start_value = tk.IntVar()
        self.subim_x_start_entry = ttk.Entry(self.subim_op_frame, textvariable=self.subim_x_start_value, width=6)
        self.subim_x_length_label = ttk.Label(self.subim_op_frame, text="Comprimento")
        self.subim_x_length_value = tk.IntVar()
        self.subim_x_length_entry = ttk.Entry(self.subim_op_frame, textvariable=self.subim_x_length_value, width=6)
        self.subim_y_start_label = ttk.Label(self.subim_op_frame, text="Início(y)")
        self.subim_y_start_value = tk.IntVar()
        self.subim_y_start_entry = ttk.Entry(self.subim_op_frame, textvariable=self.subim_y_start_value, width=6)
        self.subim_y_length_label = ttk.Label(self.subim_op_frame, text="Comprimento")
        self.subim_y_length_value = tk.IntVar()
        self.subim_y_length_entry = ttk.Entry(self.subim_op_frame, textvariable=self.subim_y_length_value, width=6)
        self.subim_op_button = ttk.Button(self.subim_op_frame, text="Selecionar", command=self._do_subim)

        self.flips_frame = ttk.Labelframe(self.buttons_frame, text="Inversões")
        self.flip_vertically_button = ttk.Button(self.flips_frame, text="Vertical", command=self._flip_vertically)
        self.flip_horizontally_button = ttk.Button(self.flips_frame, text="Horizontal", command=self._flip_horizontally)

        self.grayscale_button = ttk.Button(self.buttons_frame, text="Escala de cinza", command=self._to_grayscale, width=27)
        self.negative_button = ttk.Button(self.buttons_frame, text="Negativo", command=self._to_negative, width=27)

        self.limiar_value = tk.IntVar(value=127)
        self.limiar_entry = ttk.Entry(self.buttons_frame, textvariable=self.limiar_value, width=27)
        self.limiarize_button = ttk.Button(self.buttons_frame, text="Limiarizar", command=self._limiarize, width=27)

        self.histogram_button = ttk.Button(self.buttons_frame, text="Eq. Histograma", command=self._equalize_histogram, width=27)

        self.btw_img_ops = ttk.Labelframe(self.buttons_frame, text="Operações entre imagens")
        self.sum_images_button = ttk.Button(self.btw_img_ops, text="Somar imagens", command=self._sum_images)
        self.subt_images_button = ttk.Button(self.btw_img_ops, text="Subtrair imagens", command=self._subt_images)
        self.concat_button = ttk.Button(self.btw_img_ops, text="Concatenar", command=self._concat_images)
        self.blending_value = tk.IntVar(value=50)
        self.blending_label = ttk.Label(self.btw_img_ops, text=f"Blending: {int(self.blending_value.get())}%", width=27, anchor='w')
        self.blending_slider = ttk.Scale(self.btw_img_ops, from_=0, to=100, orient='horizontal', variable=self.blending_value)
        self.blending_slider.bind("<ButtonRelease-1>", self._blending)
        self.blending_slider.bind("<Button1-Motion>", lambda event: self.blending_label.config(text=f"Blending: {int(self.blending_value.get())}%"))

        self.brightness_value = tk.IntVar(value=0)
        self.brightness_label = ttk.Label(self.buttons_frame, text=f"Brilho: {int(self.brightness_value.get())}%", width=27, anchor='w')
        self.brightness_slider = ttk.Scale(self.buttons_frame, from_=-100, to=100, orient='horizontal', variable=self.brightness_value)
        self.brightness_slider.bind("<ButtonRelease-1>", self._brightness)
        self.brightness_slider.bind("<Button1-Motion>", lambda event: self.brightness_label.config(text=f"Brilho: {int(self.brightness_value.get())}%"))

        self.contrast_value = tk.IntVar(value=0)
        self.contrast_label = ttk.Label(self.buttons_frame, text=f"Contraste: {int(self.contrast_value.get())}%", width=27, anchor='w')
        self.contrast_slider = ttk.Scale(self.buttons_frame, from_=-100, to=100, orient='horizontal', variable=self.contrast_value)
        self.contrast_slider.bind("<ButtonRelease-1>", self._contrast)
        self.contrast_slider.bind("<Button1-Motion>", lambda event: self.contrast_label.config(text=f"Contraste: {int(self.contrast_value.get())}%"))

        self.binary_btns_frame = ttk.Labelframe(self.buttons_frame, text="Operações binárias")
        self.not_button = ttk.Button(self.binary_btns_frame, text="NOT", command=self._not)
        self.and_button = ttk.Button(self.binary_btns_frame, text="AND", command=self._and)
        self.or_button = ttk.Button(self.binary_btns_frame, text="OR", command=self._or)
        self.xor_button = ttk.Button(self.binary_btns_frame, text="XOR", command=self._xor)

        self.filters_frame = ttk.Labelframe(self.buttons_frame, text="Filtros")
        self.mask_size_frame = ttk.Labelframe(self.filters_frame, text="Tamanho da máscara")
        self.mask_size_value = tk.IntVar(value=3)
        self.mask_size_3x3 = ttk.Radiobutton(self.mask_size_frame, text="3x3", variable=self.mask_size_value, value=3)
        self.mask_size_5x5 = ttk.Radiobutton(self.mask_size_frame, text="5x5", variable=self.mask_size_value, value=5)
        self.mask_size_7x7 = ttk.Radiobutton(self.mask_size_frame, text="7x7", variable=self.mask_size_value, value=7)
        self.mask_size_9x9 = ttk.Radiobutton(self.mask_size_frame, text="9x9", variable=self.mask_size_value, value=9)
        self.mask_size_11x11 = ttk.Radiobutton(self.mask_size_frame, text="11x11", variable=self.mask_size_value, value=11)
        self.min_button = ttk.Button(self.filters_frame, text="MIN", command=self._min)
        self.max_button = ttk.Button(self.filters_frame, text="MAX", command=self._max)
        self.mean_button = ttk.Button(self.filters_frame, text="MEAN", command=self._mean)
        self.median_button = ttk.Button(self.filters_frame, text="MEDIAN", command=self._median)

        self.order_filter_frame = ttk.Frame(self.filters_frame)
        self.order_value = tk.IntVar(value=0)
        self.order_entry = ttk.Entry(self.order_filter_frame, textvariable=self.order_value)
        self.order_button = ttk.Button(self.order_filter_frame, text="ORDER", command=self._order)

        self.conservative_suavization_button = ttk.Button(self.filters_frame, text="Suav. Conservativa", command=self._conservative_suavization)

        self.gaussian_filter_frame = ttk.Frame(self.buttons_frame)
        self.gaussian_filter_frame.columnconfigure(0, weight=4)
        self.gaussian_filter_frame.columnconfigure(1, weight=1)
        self.gaussian_filter_sigma_value = tk.DoubleVar(value=0.1)
        self.gaussian_filter_sigma_entry = ttk.Entry(self.gaussian_filter_frame, textvariable=self.gaussian_filter_sigma_value, width=5, justify='right')
        self.gaussian_filter_button = ttk.Button(self.gaussian_filter_frame, text="Filtro gaussiano", command=self._gaussian_filter)

        self.border_detection_frame = ttk.Labelframe(self.buttons_frame, text="Detecção de borda")
        self.prewitt_button = ttk.Button(self.border_detection_frame, text="Prewitt", command=self._border_detection('prewitt'))
        self.sobel_button = ttk.Button(self.border_detection_frame, text="Sobel", command=self._border_detection('sobel'))
        self.laplace_button = ttk.Button(self.border_detection_frame, text="Laplace", command=self._border_detection('laplace'))

        self.morphologic_ops_frame = ttk.Labelframe(self.buttons_frame, text="Operações morfológicas")
        self.dilation_button = ttk.Button(self.morphologic_ops_frame, text="Dilatação", command=self._dilation)

    def _config(self) -> None:
        self.root.title("Processamento de Imagem")
        self.frame.grid()
        self.input_img_frame.grid(column=0, row=0, sticky='n')
        self.input_img_label.grid(column=0, row=0, padx=20, pady=20)
        self.buttons_frame.grid(column=2, row=0, rowspan=10, sticky='n')
        self.output_img_frame.grid(column=3, row=0, sticky='n')
        self.output_img_label.grid(column=0, row=0, padx=20, pady=20)
        self.open_button.grid(column=0)

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

            self.arithmetic_ops_frame.grid(column=0, sticky='we')
            self.addition_button.grid(column=0, row=0, sticky='we')
            self.addition_entry.grid(column=1, row=0, sticky='e')
            self.subtraction_button.grid(column=0, row=1, sticky='we')
            self.subtraction_entry.grid(column=1, row=1, sticky='e')
            self.multiplication_button.grid(column=0, row=2, sticky='we')
            self.multiplication_entry.grid(column=1, row=2, sticky='e')
            self.division_button.grid(column=0, row=3, sticky='we')
            self.division_entry.grid(column=1, row=3, sticky='e')

            self.subim_op_frame.grid(column=0, sticky='we')
            self.subim_op_frame.columnconfigure(0, weight=1)
            self.subim_op_frame.columnconfigure(1, weight=1)
            self.subim_op_frame.columnconfigure(2, weight=1)
            self.subim_op_frame.columnconfigure(3, weight=1)
            self.subim_x_start_label.grid(column=0, row=0)
            self.subim_x_start_entry.grid(column=1, row=0, sticky='we')
            self.subim_x_length_label.grid(column=2, row=0)
            self.subim_x_length_entry.grid(column=3, row=0, sticky='we')
            self.subim_y_start_label.grid(column=0, row=1)
            self.subim_y_start_entry.grid(column=1, row=1, sticky='we')
            self.subim_y_length_label.grid(column=2, row=1)
            self.subim_y_length_entry.grid(column=3, row=1, sticky='we')
            self.subim_op_button.grid(column=2, row=2, columnspan=2, sticky='e')

            self.flips_frame.grid(column=0, sticky='we')
            self.flip_vertically_button.pack(side='left', expand=True, fill='x')
            self.flip_horizontally_button.pack(side='left', expand=True, fill='x')

            self.grayscale_button.grid(column=0)
            self.negative_button.grid(column=0)
            self.histogram_button.grid(column=0)
            self.brightness_label.grid(column=0)
            self.brightness_slider.grid(column=0, sticky="we")
            self.contrast_label.grid(column=0)
            self.contrast_slider.grid(column=0, sticky="we")

            self.gaussian_filter_frame.grid(column=0, sticky='we')
            self.gaussian_filter_button.grid(column=0, row=0, sticky='we')
            self.gaussian_filter_sigma_entry.grid(column=1, row=0, sticky='e')

            self.border_detection_frame.grid(column=0, sticky='we')
            self.prewitt_button.pack(side='left', expand=True, fill='x')
            self.sobel_button.pack(side='left', expand=True, fill='x')
            self.laplace_button.pack(side='left', expand=True, fill='x')
            
            self.morphologic_ops_frame.grid(column=0, sticky='we')
            self.dilation_button.pack(side='left', expand=True, fill='x')

            self.save_button.grid(column=0, row=1)
            self.reset_button.grid(column=0, row=2)

            self.limiar_entry.grid(column=0)
            self.limiarize_button.grid(column=0)

            self.binary_btns_frame.grid(column=0, sticky='we')
            self.not_button.pack(side='left', expand=True)
            self.and_button.pack(side='left', expand=True)
            self.or_button.pack(side='left', expand=True)
            self.xor_button.pack(side='left', expand=True)

            self.filters_frame.grid(column=0, sticky='we')
            self.min_button.grid(column=0, row=0, sticky='we')
            self.mean_button.grid(column=0, row=1, sticky='we')
            self.max_button.grid(column=1, row=0, sticky='we')
            self.median_button.grid(column=1, row=1, sticky='we')
            self.conservative_suavization_button.grid(column=0, columnspan=2, row=2, sticky='we')

            self.order_filter_frame.grid(column=0, row=3, columnspan=2, sticky='we')
            self.order_entry.grid(column=0, row=0, sticky='we')
            self.order_button.grid(column=1, row=0, sticky='we')

            self.mask_size_frame.grid(column=0, columnspan=2, sticky='we')
            self.mask_size_3x3.grid(column=0, row=0, padx=2)
            self.mask_size_5x5.grid(column=1, row=0, padx=2)
            self.mask_size_7x7.grid(column=2, row=0, padx=2)
            self.mask_size_9x9.grid(column=3, row=0, padx=2)
            self.mask_size_11x11.grid(column=4, row=0, padx=2)

        except:
            print("imagem não selecionada")

    def _select_image_2(self) -> None:
        """Action of the open button"""
        try:
            filename = self._openfilename()

            self.input_img2 = Image.open(filename) # open image with pillow
            self.open_button2.grid_remove()

            self.input_img2_frame.grid(column=1, row=0, sticky='n')
            self.input_img2_label.grid(column=0, row=0, padx=20, pady=20)

            # shows input image in the label
            self._show_image(self.input_img2, self.input_img2_label)

            self.change_img2_button.grid(column=0, row=1)
            self.remove_img2_button.grid(column=0, row=2)

            self.btw_img_ops.grid(column=0, sticky='we')
            self.btw_img_ops.columnconfigure(0, weight=1)
            self.btw_img_ops.columnconfigure(1, weight=1)
            self.sum_images_button.grid(column=0, row=0, sticky='we')
            self.subt_images_button.grid(column=1, row=0, sticky='we')
            self.concat_button.grid(column=0, row=1, sticky='we')
            self.blending_label.grid(column=0, columnspan=2, row=2, sticky='we')
            self.blending_slider.grid(column=0, columnspan=2, row=3, sticky='we')

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

        self.input_img2_frame.grid_remove()

    def _to_negative(self) -> None:
        """Convert the base image pixels to negative"""
        negative_image = process.to_negative(self.input_img)

        self.output_img.putdata(negative_image)

        self._show_image(self.output_img, self.output_img_label)

    def _to_grayscale(self):
        """Convert the input image to grayscale"""

        grayscale_img = None

        if (self.input_img.mode != 'L'):
            image = self.input_img
            grayscale_img_data = process.to_grayscale(image)

            grayscale_img = Image.new('L', image.size)
            grayscale_img.putdata(grayscale_img_data)

        else:
            grayscale_img = self.input_img.copy()

        self.output_img = grayscale_img

        self._show_image(self.output_img, self.output_img_label)

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
            filetypes=filetypes,
            defaultextension=filetypes
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
        image = self.input_img
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
        image = self.input_img
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

        img_parent = image_label.grid_info()['in']
        img_col = image_label.grid_info()['column']

        img_histogram_data = process.get_histogram(image)
        self._plot_histogram(histogram_data=img_histogram_data, column=0, row=10, frame=img_parent)

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
        image = self.input_img

        if (image.mode != 'L'):
            grayscale_img = Image.new('L', image.size)
            grayscale_img.putdata(process.to_grayscale(image))

            image = grayscale_img.copy()

        binary_img_data = process.binarize(image, self.limiar_value.get())

        binary_img = Image.new('1', image.size)
        binary_img.putdata(binary_img_data)

        self.output_img = binary_img
        self._show_image(self.output_img, self.output_img_label)

    def _plot_histogram(self, histogram_data, column, row, frame):
        # create a figure
        figure = Figure(figsize=(4, 2), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, frame)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar([i for i in range(256)], histogram_data)

        figure_canvas.get_tk_widget().grid(column=column, row=row, padx=5, pady=5)

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

    def _not(self):
        im = self.input_img

        if (im.mode != '1'):
            out_im = im

            if (im.mode != 'L'):
                grayscale_im_data = process.to_grayscale(im)

                out_im = Image.new('L', im.size)
                out_im.putdata(grayscale_im_data)

            binary_im_data = process.binarize(out_im)
            out_im = Image.new('1', out_im.size)
            out_im.putdata(binary_im_data)

            out_im_data = process.not_(out_im)
            out_im.putdata(out_im_data)

            self.output_img = out_im
        else:
            self.output_img.putdata(process.not_(im))

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

    def _xor(self):
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
        out_im_data = process.xor_(im1, im2)
        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _min(self):
        im = self.input_img

        out_im = Image.new(im.mode, im.size)
        out_im_data = process.filter(im, 'min', mask_size=self.mask_size_value.get())

        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _max(self):
        im = self.input_img

        out_im = Image.new(im.mode, im.size)
        out_im_data = process.filter(im, 'max', mask_size=self.mask_size_value.get())

        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _mean(self):
        im = self.input_img

        out_im = Image.new(im.mode, im.size)
        out_im_data = process.filter(im, 'mean', mask_size=self.mask_size_value.get())

        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _median(self):
        im = self.input_img

        out_im = Image.new(im.mode, im.size)
        out_im_data = process.filter(im, 'median', mask_size=self.mask_size_value.get())

        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _order(self):
        im = self.input_img

        out_im = Image.new(im.mode, im.size)

        try:
            out_im_data = process.filter(im, 'order', mask_size=self.mask_size_value.get(), index=self.order_value.get())

            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        except IndexError:
            showinfo("IndexError", "Índice inexistente")

    def _conservative_suavization(self):
        im = self.input_img

        out_im = Image.new(im.mode, im.size)
        out_im_data = process.conservative_suavization(im, mask_size=self.mask_size_value.get())

        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _gaussian_filter(self):
        im = self.input_img

        out_im = Image.new(im.mode, im.size)
        out_im_data = process.gaussian_filter(im, sigma=self.gaussian_filter_sigma_value.get())

        out_im.putdata(out_im_data)

        self.output_img = out_im

        self._show_image(self.output_img, self.output_img_label)

    def _do_arithmetic_op(self, op):

        def addition():
            im = self.input_img
            out_im_data = process.arithmetic(im, self.addition_value.get(), '+')
            out_im = Image.new(im.mode, im.size)
            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        def subtraction():
            im = self.input_img
            out_im_data = process.arithmetic(im, self.subtraction_value.get(), '-')
            out_im = Image.new(im.mode, im.size)
            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        def multiplication():
            im = self.input_img
            out_im_data = process.arithmetic(im, self.multiplication_value.get(), '*')
            out_im = Image.new(im.mode, im.size)
            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        def division():
            im = self.input_img
            out_im_data = process.arithmetic(im, self.division_value.get(), '/')
            out_im = Image.new(im.mode, im.size)
            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        if (op == '+'):
            return addition
        if (op == '-'):
            return subtraction
        if (op == '*'):
            return multiplication
        if (op == '/'):
            return division

    def _do_subim(self):
        im = self.input_img

        start = (self.subim_x_start_value.get(), self.subim_y_start_value.get())
        length = (self.subim_x_length_value.get(), self.subim_y_length_value.get())

        try:
            out_im_data = process.subim(im, start, length)
            out_im = Image.new(im.mode, (length[0], length[1]))
            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)
        except IndexError:
            showerror("IndexError", "Impossível selecionar imagem.")
        except ZeroDivisionError:
            showerror("ZeroDivisionError", "Tamanho da imagem resultante é zero. Modifique os valores.")
        except ValueError:
            showerror("ValueError", "Tamanho da imagem resultante é zero. Modifique os valores.")

    def _border_detection(self, method):
        def prewitt():
            im = self.input_img

            out_im = Image.new(im.mode, im.size)
            out_im_data = process.border_detection(im, 'prewitt')

            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        def sobel():
            im = self.input_img

            out_im = Image.new(im.mode, im.size)
            out_im_data = process.border_detection(im, 'sobel')

            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        def laplace():
            im = self.input_img

            out_im = Image.new(im.mode, im.size)
            out_im_data = process.border_detection(im, 'laplace')

            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        methods_map = {
            'prewitt': prewitt,
            'sobel': sobel,
            'laplace': laplace
        }

        return methods_map[method]

    def _dilation(self):
        im = self.input_img

        if im.mode != '1':
            if (im.mode != 'L'):
                grayscale_im = Image.new('L', im.size)
                grayscale_im_data = process.to_grayscale(im)
                grayscale_im.putdata(grayscale_im_data)

                im = grayscale_im
            
            binary_im = Image.new('1', im.size)
            binary_im_data = process.binarize(im)
            binary_im.putdata(binary_im_data)

            im = binary_im

        try:
            out_im = Image.new(im.mode, im.size)
            out_im_data = process.dilation(im)

            out_im.putdata(out_im_data)

            self.output_img = out_im

            self._show_image(self.output_img, self.output_img_label)

        except TypeError:
            showerror("Imagem inválida", "A imagem precisa ser binária")

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
