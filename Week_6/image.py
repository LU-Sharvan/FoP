"""
File: image.py
Author: Sharvan Gangadin
Description: Image Processor for pixelating and blurring images among other uses
License: LU license
"""

# Importing dependencies
import numpy as np
from PIL import Image
import copy
import pickle
import matplotlib.pyplot as plt

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.color_mapping = None
        self.is_RGB = None  # False means color mapping

    # Small helpers

    def is_RGB_mode(self):
        return self.is_RGB

    def get_color_map(self):
        return self.color_mapping

    def get_array(self):
        if self.image is None:
            return None
        return np.array(self.image)

    def check_image_loaded(self):
        if self.image is None:
            raise ValueError("No loaded image")

    def shape(self):
        self.check_image_loaded()
        return self.image.shape[0], self.image.shape[1]

    def add_extension(self, filepath, ext):
        if not filepath.endswith(ext):
            return filepath + ext
        return filepath

    def load(self, filepath):
        # PNG file: RGB values
        if filepath.endswith(".png"):
            with Image.open(filepath) as image_png_raw:
                image_png = image_png_raw.convert("RGB")
 
            # Redefining properties
            self.image = np.array(image_png)
            self.color_mapping = None
            self.is_RGB = True

        # Pickle file: color map
        elif filepath.endswith("pkl"):
            with open(filepath, "rb") as image_pkl_raw:
                image_pkl, color_mapping = pickle.load(image_pkl_raw)
  
            # Redefining properties
            self.image = image_pkl
            self.color_mapping = color_mapping
            self.is_RGB = False

        # Error with another extension
        else:
            raise ValueError("Image contains unsupported extension")

    def save(self, filepath):
        self.check_image_loaded()

        # PNG file: for images
        if self.is_RGB:
            path = self.add_extension(filepath, ".png")
            image = Image.fromarray(self.image)
            image.save(path)  # Save with name of file/filepath

        # Picle file: for color map
        else:
            path = self.add_extension(filepath, ".pkl")
            with open(path, "wb") as file:
                pickle.dump((self.image, self.color_mapping), file)

    # RGB <-> colormap helpers

    def compute_bins(self, img, bins):
        # Each channel scaled into bins: range 0..255 -> [0,1]
        r_bin = (img[:, :, 0].astype(np.int64) * bins) // 256
        g_bin = (img[:, :, 1].astype(np.int64) * bins) // 256
        b_bin = (img[:, :, 2].astype(np.int64) * bins) // 256
        return r_bin, g_bin, b_bin

    def ids_dtype(self, ids):
        # Choose more efficient storage type based on the highest ID
        max_id = int(ids.max())  # Turning Numpy scalar into Python integer

        if max_id <= 255:
            return ids.astype(np.uint8)  # 1 byte per pixel
       
        elif max_id <= 65535:
            return ids.astype(np.uint16)  # 2 bytes per pixel

        return ids.astype(np.uint32)  # Otherwise 4 bytes per pixel

    def _build_color_map(self, unique_ids, flat_groups, flat_pixels):
        color_map = {}
 
        # Each unique ID gets the mean RGB color of its pixel group
        for new_id, old_id in enumerate(unique_ids):
            mask = (flat_groups == old_id)  # Pixels in flat_groups of old_id group become True
            mean_color = flat_pixels[mask].mean(axis=0)  # Avg of all pizels in group row
            color_map[int(new_id)] = mean_color  # Dicitionary entry: Id is key and mean is value
        return color_map

    def _rgb_to_colormap(self, bins):
        img = self.image.astype(np.int64)  # Work with integers: 0-255 RGB
        h, w, _ = img.shape  # Original image dimensions

        # Step 1: Create bins for R, G, B with helper function
        r_bin, g_bin, b_bin = self.compute_bins(img, bins)

        # Step 2: Unique group index per pixel based on self-defined weight
        group = r_bin * (bins ** 2) + g_bin * bins + b_bin  # To the power 2, 1, 0

        # Step 3: Flatten pixel data for grouping
        flat_groups = group.reshape(-1)  # 1D list of group IDs
        flat_pixels = img.reshape(-1, 3) / 255.0  # RGB values converted to floats in [0,1]

        # Step 4: Unique groups + reindexing (Unique groups can have gaps)
        unique_ids, inverse = np.unique(flat_groups, return_inverse=True)  # Solely unique group IDs
        reindexed = inverse.reshape(h, w)  # Matrix with IDs for groups

        # Step 5: Build the color_map using new IDs
        color_map = self._build_color_map(unique_ids, flat_groups, flat_pixels)

        # Step 6: Redefining properties
        self.image = self.ids_dtype(reindexed)
        self.color_mapping = color_map
        self.is_RGB = False

    def _colormap_to_rgb(self):
        ids = self.image  # Every integer in the color map is an ID for a RGB value
        h, w = ids.shape  # Dimensions of the 2D array

        # Making empty RGB matrix of same dimensions as RGB image
        rgb = np.zeros((h, w, 3), dtype=np.uint8)  # RGB has to be uint8

        for id_, color in self.color_mapping.items():
            # Color stored as float in [0,1] and now converted to 0-255 RGB
            r = int(color[0] * 255)
            g = int(color[1] * 255)
            b = int(color[2] * 255)

            mask = (ids == id_)  # True where color map ID is equal to ID of calculated
            rgb[mask] = (r, g, b)  # Img gets colored in with (r,g,b) triple

        self.image = rgb
        self.color_mapping = None
        self.is_RGB = True

    def change_image_format(self, format_, bins=2):
        self.check_image_loaded()  # Checking for errors

        # Defining when RGB and Color map can be Truthy or Falsy
        rgb = format_ is False and self.is_RGB
        color_map = format_ is True and not self.is_RGB

        # Base case without toggle function
        # Format = True -> We want RGB
        # Format = False -> We want color map
        if format_ == self.is_RGB:
            return  # No changes

        if rgb:  # RGB -> Color map
            self._rgb_to_colormap(bins)

        elif color_map:  # Color map -> RGB
            self._colormap_to_rgb()
    
    def toggle_format(self, bins=2):
        # If currently RGB → convert to colormap.
        # If currently colormap → convert to RGB.
        self.change_image_format(not self.is_RGB, bins=bins)

    # Color rotation helpers

    def _rotate_rgb_colors(self):
        r = self.image[:, :, 0].copy()
        g = self.image[:, :, 1].copy()
        b = self.image[:, :, 2].copy()
        self.image[:, :, 0] = g  # R = G
        self.image[:, :, 1] = b  # G = B
        self.image[:, :, 2] = r  # B = R

    def _rotate_colormap_colors(self):
        # Error check
        if self.color_mapping is None:
            raise ValueError("No color map")

        old = copy.deepcopy(self.color_mapping)
        keys = sorted(old.keys())  # Sorted list of color map IDs
        n = len(keys)  # Number of colors
        for key in keys:
            self.color_mapping[(key + 1) % n] = old[key]

    def rotate_colors(self):
        self.check_image_loaded()
        if self.is_RGB:  # RGB
            self._rotate_rgb_colors()
        else:  # Color map
            self._rotate_colormap_colors()

    # Blur helpers

    def blur_array(self, img, size):
        h, w, _ = img.shape  # Array: (highth, width, channels)
        blurred = np.zeros_like(img)  # Returns array with properties of img but with zeros
        radius = size // 2  # Blur radius: you're at the center and then this many pixels around you

        for i in range(h):  # Loops through rows
            for j in range(w):  # Loops through columns
                row_1 = max(0, i - radius)
                row_2 = min(h, i + radius + 1)
                column_1 = max(0, j - radius)
                column_2 = min(w, j + radius + 1)

                region = img[row_1:row_2, column_1:column_2]  # Region of img with rows and columns as borders
                blurred[i, j] = region.mean(axis=(0, 1))  # All values of array in region become the mean value

        return blurred  # Blurred img

    def blur_RGB_images(self, size=3):
        self.check_image_loaded()

        if not self.is_RGB:  # Not possible for color map
            return
        self.image = self.blur_array(self.image, size)

    # Pixelate helpers

    def limit_area(self, area):
        (xmin, xmax), (ymin, ymax) = area
        shape = self.image.shape  # Array: (highth, width, channels)

        if len(shape) == 3:
            h, w = shape[0], shape[1]
        else:
            h, w = shape

        xmin = max(0, xmin)  # Left
        ymin = max(0, ymin)  # Top
        xmax = min(w, xmax)  # Right
        ymax = min(h, ymax)  # Bottom
        return xmin, xmax, ymin, ymax

    def pixelate_region(self, xmin, xmax, ymin, ymax, size):
        for y in range(ymin, ymax, size):  # Loop through rows with size preventing overlap
            for x in range(xmin, xmax, size):  # Loop through colomns within rows with size preventing overlap
                row_1, row_2 = y, min(y + size, ymax)
                column_1, column_2 = x, min(x + size, xmax)

                # Block/pixel of all values between rows and columns
                block = self.image[row_1:row_2, column_1:column_2]

                # RGB
                if self.is_RGB:  # Changing RGB values
                    mean_color = block.mean(axis=(0, 1))  # Mean of rows and columns, not of RGB channels
                    self.image[row_1:row_2, column_1:column_2] = mean_color  # Values in block get replaced by mean

                # Color map
                else:  # Changing IDs
                    flat = block.reshape(-1)  # Forms the block as a list
                    counts = np.bincount(flat)  # Counts individual IDs
                    mode_id = counts.argmax()  # Returns most counted ID
                    self.image[row_1:row_2, column_1:column_2] = mode_id  # IDs in block become most counted one

    def pixelate_images(self, area, size=10):
        self.check_image_loaded()
        xmin, xmax, ymin, ymax = self.limit_area(area)
        self.pixelate_region(xmin, xmax, ymin, ymax, size)

    def show(self, filename=None):
        if self.is_RGB_mode():
            img = self.get_array()
        else:
            img = np.vectorize(self.get_color_map().get, signature='()->(n)')(self.get_array())

        plt.imshow(img, interpolation='none')
        plt.axis('off')
        if filename is not None:
            plt.savefig(filename + ".png", bbox_inches='tight', pad_inches=0)
        else:
            plt.show()

if __name__ == "__main__":
    img = ImageProcessor()
    img.load("pumpkin.png")
    area = ((0, img.shape()[1]), (0, img.shape()[0]))  # Pixelate (columns, rows) with x, y min/max coordinates possible
    img.pixelate_images(area, size=10)
    img.save("pumpkin_masked.png") 
