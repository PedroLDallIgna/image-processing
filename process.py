from ast import Tuple
from math import floor
from PIL import Image
import math

def get_max_and_min(data):
    """Returns a tuple with min and max value of a list (image color band)"""
    return (min(data), max(data))

def get_image_data(im):
    """Returns a list with flattened data of each color band"""
    return [list(im.getdata(band)) for band in [i for i in range(len(im.getbands()))]]

def reflat_data(unflat_data: list):
    """Returns a flattened image data containing a tuple with pixel values"""
    flattened_data = []
    for i in range(len(unflat_data[0])):
        pixel = []
        for j in range(len(unflat_data)):
            pixel.append(unflat_data[j][i])

        # verify if have more bands
        if (len(unflat_data) > 1):
            flattened_data.append(tuple(pixel))
        else:
            flattened_data.append(pixel[0])

    return flattened_data

def sum_images(im1, im2):
    if (im1.mode != im2.mode):
        raise Exception("The images modes are different")

    # resize the second image case they don't have the same size
    if (im1.width != im2.width or im1.height != im2.height):
        im2 = im2.resize(im1.size, Image.Resampling.LANCZOS)

    mins_maxs = []
    out_im_data = []

    # sums the pixels for each color band
    for b in range(len(im1.getbands())):
        out_im_data.append([])
        
        # get images data (pixels)
        im1_band_data = list(im1.getdata(b))
        im2_band_data = list(im2.getdata(b))

        # sum the pixels
        for i in range(len(im1_band_data)):
            out_im_data[b].append(im1_band_data[i] + im2_band_data[i])

        # gets the max and min value of each color band
        mins_maxs.append(get_max_and_min(out_im_data[b]))

    # gets the normalized pixel for each color band
    for b in range(len(out_im_data)):
        for i in range(len(out_im_data[b])):
            out_im_data[b][i] = round(255 / (mins_maxs[b][1] - mins_maxs[b][0]) * (out_im_data[b][i] - mins_maxs[b][0]))

    # returns the flatted data
    return reflat_data(out_im_data)

def get_histogram(im):
    im_data = get_image_data(im)

    histogram = [0 for i in range(256)]

    for band in range(len(im_data)):
        for pixel_i in im_data[band]:
            histogram[pixel_i] += 1

    return histogram

def get_cfd(histogram_data):
    # get cumulative distribution frequency
    cfd = [0 for i in range(256)]

    cfd[0] = histogram_data[0]
    for i in range(1, len(cfd)):
        cfd[i] = cfd[i-1] + histogram_data[i]

    return cfd

def equalize_histogram(im):
    out_im_data = get_image_data(im)

    histogram_data = get_histogram(im)

    cfd = get_cfd(histogram_data)

    # transforms image pixels
    for band in range(len(out_im_data)):
        for i in range(len(out_im_data[band])):
            pixel_value = out_im_data[band][i]
            out_im_data[band][i] = round((cfd[pixel_value] - min(cfd)) / ((im.height*im.width) - min(cfd)) * 255)

    # returns the flatted data
    return reflat_data(out_im_data)

def unflat_data(flattened_data, height, width):
    """Transforms the flat image data list (unidimensional) into an unflat (bidimensinal) image data list"""
    return [flattened_data[row*width:(row+1)*width] for row in range(height)]

def flat_data(unflattened_data):
    """Transforms the unflat image data list (bidimensional) into a flat (unidimensional) image data list"""
    flattened_data = []
    for row in unflattened_data:
        flattened_data += row

    return flattened_data

def concat_images(im1, im2):
    """Concat both images (side by side) and return as flattened data"""
    if (im1.mode != im2.mode):
        raise Exception("The images modes are different")

    # resize the second image case they don't have the same size
    if (im1.height != im2.height):
        im2 = im2.resize((im1.height, im2.width), Image.Resampling.LANCZOS)

    im1_data = unflat_data(list(im1.getdata()), im1.height, im1.width)
    im2_data = unflat_data(list(im2.getdata()), im2.height, im2.width)

    out_im_data = []
    for row in range(len(im1_data)):
        concatened_row = []
        concatened_row += im1_data[row]
        concatened_row += im2_data[row]
        out_im_data.append(concatened_row)

    return flat_data(out_im_data)

def change_brightness(im, brightness_value):
    img_data = list(im.getdata())

    out_img_data = []

    for pixel_i in range(len(img_data)):
        if (type(img_data[pixel_i]) == tuple): 
            new_pixel = []
            for color_i in range(len(img_data[pixel_i])):
                new_color = round(img_data[pixel_i][color_i] + brightness_value)
                if (new_color > 255):
                    new_pixel.append(255)
                elif (new_color < 0):
                    new_pixel.append(0)
                else:
                    new_pixel.append(new_color)
            out_img_data.append(tuple(new_pixel))
        else:
            new_color = round(img_data[pixel_i] + brightness_value)
            if (new_color > 255):
                new_color = 255
            elif (new_color < 0):
                new_color = 0
            out_img_data.append(new_color)

    return out_img_data

def change_contrast(im, contrast_value):
    img_data = get_image_data(im)

    out_img_data = []

    for band_i in range(len(img_data)):
        out_img_data.append([])
        new_pixel = []
        for pixel_i in range(len(img_data[band_i])):
            new_pixel = round(img_data[band_i][pixel_i] * contrast_value)
            if (new_pixel > 255):
                new_pixel = 255
            elif (new_pixel < 0):
                new_pixel = 0
            out_img_data[band_i].append(new_pixel)

    return reflat_data(out_img_data)

def blend(im1, im2, blend_value):
    # resize the second image case they don't have the same size
    if (im1.height != im2.height):
        im2 = im2.resize((im1.height, im2.width), Image.Resampling.LANCZOS)

    im1_data = get_image_data(im1)
    im2_data = get_image_data(im2)
    out_im_data = [] 

    for band_i in range(len(im1_data)):
        out_im_data.append([])
        for pixel_i in range(len(im1_data[band_i])):
            new_pixel = blend_value * im1_data[band_i][pixel_i] + (1 - blend_value) * im2_data[band_i][pixel_i]
            if (new_pixel > 255):
                new_pixel = 255
            elif (new_pixel < 0):
                new_pixel = 0
            out_im_data[band_i].append(round(new_pixel))

    return reflat_data(out_im_data)

def to_grayscale(im):
    im_data = get_image_data(im)

    out_im_data = []
    out_im_data.append([])

    for pixel_i in range(len(im_data[0])):
        pixel_sum = 0
        for band_i in range(len(im_data)):
            pixel_sum += im_data[band_i][pixel_i]

        new_pixel = pixel_sum / len(im_data)
        out_im_data[0].append(new_pixel)

    return reflat_data(out_im_data)

def to_negative(im):
    """Receives an image and negate it"""
    im_data = get_image_data(im)
    out_im_data = []
    
    for band in range(len(im_data)):
        out_im_data.append([])
        for pixel in range(len(im_data[band])):
            negative_pixel = 255 - im_data[band][pixel]
            out_im_data[band].append(negative_pixel)
            
    return reflat_data(out_im_data)

def binarize(im, limiar_value=127):
    """Receives a grayscale image and binarize it"""
    im_data = get_image_data(im)
    out_im_data = []

    for band_i in range(len(im_data)):
        out_im_data.append([])
        for pixel_i in range(len(im_data[band_i])):
            new_pixel = 0
            if (im_data[band_i][pixel_i] > limiar_value):
                new_pixel = 255
            else:
                new_pixel = 0
            out_im_data[band_i].append(new_pixel)

    return reflat_data(out_im_data)

def not_(im):
    """Receives a binary image and negate it"""
    im_data = get_image_data(im)
    out_im_data = []

    for band_i in range(len(im_data)):
        out_im_data.append([])
        for pixel_i in range(len(im_data[band_i])):
            out_im_data[band_i].append(0 if im_data[band_i][pixel_i] == 255 else 255)

    return reflat_data(out_im_data)

def and_(im1, im2):
    """Receives two binary images and apply AND operation in its pixels"""
    if (im1.height != im2.height):
        im2 = im2.resize((im1.height, im2.width), Image.Resampling.LANCZOS)

    im1_data = get_image_data(im1)
    im2_data = get_image_data(im2)
    out_im_data = []

    for band_i in range(len(im1_data)):
        out_im_data.append([])
        for pixel_i in range(len(im1_data[band_i])):
            new_pixel = 0
            if (im1_data[band_i][pixel_i] == 0 and im2_data[band_i][pixel_i] == 0  or im1_data[band_i][pixel_i] == 0 and im2_data[band_i][pixel_i] == 255 or im1_data[band_i][pixel_i] == 255 and im2_data[band_i][pixel_i] == 0):
                new_pixel = 0
            elif (im1_data[band_i][pixel_i] == 255 and im2_data[band_i][pixel_i] == 255):
                new_pixel = 255
            out_im_data[band_i].append(new_pixel)
    
    return reflat_data(out_im_data)

def or_(im1, im2):
    """Receives two binary images and apply OR operation in its pixels"""
    if (im1.height != im2.height):
        im2 = im2.resize((im1.height, im2.width), Image.Resampling.LANCZOS)

    im1_data = get_image_data(im1)
    im2_data = get_image_data(im2)
    out_im_data = []

    for band_i in range(len(im1_data)):
        out_im_data.append([])
        for pixel_i in range(len(im1_data[band_i])):
            new_pixel = 0
            if (im1_data[band_i][pixel_i] == 0 and im2_data[band_i][pixel_i] == 0):
                new_pixel = 0
            elif (im1_data[band_i][pixel_i] == 255 and im2_data[band_i][pixel_i] == 255 or im1_data[band_i][pixel_i] == 0 and im2_data[band_i][pixel_i] == 255 or im1_data[band_i][pixel_i] == 255 and im2_data[band_i][pixel_i] == 0):
                new_pixel = 255
            out_im_data[band_i].append(new_pixel)
    
    return reflat_data(out_im_data)

def filter(im, type, index=None, mask_size=3):

    types_map = {
        'min': min,
        'max': max,
        'mean': lambda mask: int(sum(mask) / len(mask)),
        'median': lambda mask: mask[int(len(mask) / 2) + 1],
        'order': lambda mask, index: mask[index]
    }

    if (mask_size % 2 == 0):
        raise ValueError
    mask_space = floor(mask_size / 2)
    im_data = get_image_data(im)
    out_im_data = []

    for band in range(len(im_data)):
        out_im_data.append([]) # appends an empty list for the band(r,g or b)
        for row in range(im.height):
            for col in range(im.width):
                # if initial rows, final rows, initial columns or final columns, only appends the pixel value
                if (row < mask_space or row > im.height-mask_space-1 or col < mask_space or col > im.width-mask_space-1):
                    out_im_data[band].append(im_data[band][row * im.width + col])
                
                # if not...
                else:
                    # gets the mask of the given mask size
                    mask = [im_data[band][i * im.width + j] for i in range(row-mask_space, row+mask_space+1)
                                                            for j in range(col-mask_space, col+mask_space+1)]

                    # sort the mask
                    mask.sort()

                    # get the resulting value
                    if (type == 'order'):
                        result_value = types_map[type](mask, index)
                    else:
                        result_value = types_map[type](mask)

                    # appends the minimum value
                    out_im_data[band].append(result_value)

    # return a flat list (list with tuple of pixels)
    return reflat_data(out_im_data)

def trunc_pixel(pixel):
    return 255 if pixel > 255 else (0 if pixel < 0 else pixel)

def arithmetic(im, constant, op):
    
    ops = {
        '+': lambda pixel, constant: trunc_pixel(pixel + constant),
        '-': lambda pixel, constant: trunc_pixel(pixel - constant),
        '*': lambda pixel, constant: trunc_pixel(int(pixel * constant)),
        '/': lambda pixel, constant: trunc_pixel(int(pixel / constant))
    }
    
    im_data = get_image_data(im)
    
    for band_i in range(len(im_data)):
        for pixel_i in range(len(im_data[band_i])):
            im_data[band_i][pixel_i] = ops[op](im_data[band_i][pixel_i], constant)
            
    return reflat_data(im_data)

def subim(im, start: Tuple, length: Tuple):
    im_data = get_image_data(im)

    out_im_data = []
    
    for band_i in range(len(im_data)):
        out_im_data.append([])
        for row in range(start[1], start[1] + length[1]):
            for col in range(start[0], start[0] + length[0]):
                pixel = im_data[band_i][row * im.width + col]
                
                out_im_data[band_i].append(pixel)
                
    return reflat_data(out_im_data)

def conservative_suavization(im, mask_size=3):

    if (mask_size % 2 == 0):
        raise ValueError
    mask_space = floor(mask_size / 2)
    im_data = get_image_data(im)
    out_im_data = []

    for band in range(len(im_data)):
        out_im_data.append([]) # appends an empty list for the band(r,g or b)
        for row in range(im.height):
            for col in range(im.width):
                # if initial rows, final rows, initial columns or final columns, only appends the pixel value
                if (row < mask_space or row > im.height-mask_space-1 or col < mask_space or col > im.width-mask_space-1):
                    out_im_data[band].append(im_data[band][row * im.width + col])
                
                # if not...
                else:
                    # gets the mask of the given mask size
                    mask = [im_data[band][i * im.width + j] for i in range(row-mask_space, row+mask_space+1)
                                                            for j in range(col-mask_space, col+mask_space+1)]
                    
                    # gets the central pixel value and removes from mask to not influentiate
                    pixel = im_data[band][row * im.width + col]
                    mask.remove(pixel)

                    # gets min and max values of the mask
                    min_max = (min(mask), max(mask))
                    
                    # if the pixel value is lower than the min, pixel will be min
                    if (pixel < min_max[0]):
                        pixel = min_max[0]
                    # if the pixel value is greater than the max, pixel will be max
                    elif (pixel > min_max[1]):
                        pixel = min_max[1]

                    # appends the pixel value
                    out_im_data[band].append(pixel)

    # return a flat list (list with tuple of pixels)
    return reflat_data(out_im_data)

def gaussian_filter(im, sigma):
    im_data = get_image_data(im)
    out_im_data = []

    gaussian_kernel = []
    for i in range(-2, 3):
        for j in range(-2, 3):
            coefficient = (1 / (2 * math.pi * (sigma ** 2)))
            result = coefficient * math.exp(- ((i ** 2 + j ** 2) / (2 * sigma ** 2)))
            gaussian_kernel.append(result)
    
    # sum of gaussian kernel values
    gaussian_kernel_sum = sum(gaussian_kernel)

    # normalize gaussian kernel
    for i in range(len(gaussian_kernel)):
        gaussian_kernel[i] /= gaussian_kernel_sum

    for band_i in range(len(im_data)):
        out_im_data.append([])
        for row in range(im.height):
            for col in range(im.width):
                # if initial rows, final rows, initial columns or final columns, only appends the pixel value
                if (row < 2 or row > im.height-3 or col < 2 or col > im.width-3):
                    out_im_data[band_i].append(im_data[band_i][row * im.width + col])
                
                # if not...
                else:
                    im_kernel = [im_data[band_i][x * im.width + y] for x in range(row-2, row+3)
                                                                   for y in range(col-2, col+3)]

                    for item_i in range(len(im_kernel)):
                        im_kernel[item_i] *= gaussian_kernel[item_i]

                    result_pixel = sum(im_kernel)

                    out_im_data[band_i].append(math.floor(result_pixel))

    return reflat_data(out_im_data)
