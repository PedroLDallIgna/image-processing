from PIL import Image

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

def equalize_histogram(im):
    histogram_data = cfd = [0 for i in range(256)]
    out_im_data = get_image_data(im)

    # get histogram
    for band in range(len(out_im_data)):
        for pixel_i in out_im_data[band]:
            histogram_data[pixel_i] += 1

    # get cumulative distribution frequency
    cfd[0] = histogram_data[0]
    for i in range(1, len(cfd)):
        cfd[i] = histogram_data[i-1] + histogram_data[i]

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

def negate(im):
    im_data = get_image_data(im)
    out_im_data = []

    for band_i in range(len(im_data)):
        out_im_data.append([])
        for pixel_i in range(len(im_data[band_i])):
            new_pixel = 0
            if (im_data[band_i][pixel_i] > 127):
                new_pixel = 255
            else:
                new_pixel = 0
            out_im_data[band_i].append(new_pixel)

    return reflat_data(out_im_data)

