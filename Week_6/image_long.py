# importing dependencies
import numpy as np
from PIL import Image
import copy
import pickle
import matplotlib.pyplot as plt

class ImageProcessor():
    # Your methods here

    def __init__(self):
        self.image = None
        self.color_mapping = None
        self.is_RGB = None  # False means color mapping

    def is_RGB_mode(self):
        return self.is_RGB

    def get_color_map(self):
        return self.color_mapping

    def get_array(self):
        # Check if image is present
        if self.image is None:
            return None  # To prevent TypeError as None will still make an array

        return np.array(self.image)

    def shape(self):
        # Check if image is present
        if self.image is None:
            raise ValueError("No loaded image")

        # shape returns x, y from the x, y, z axis of the image
        return self.image.shape[0], self.image.shape[1]

    def load(self, filepath):
        # .png files contain information for RGB
        if filepath.endswith(".png"):
            with Image.open(filepath) as image_png_raw:
                image_png = image_png_raw.convert("RGB")  # Forces image to get 3 RGB channels

            # Sets values for RGB
            self.image = np.array(image_png)
            self.color_mapping = None
            self.is_RGB = True

        # .pkl files contain information for color mapping
        elif filepath.endswith(".pkl"):
            with open(filepath, "rb") as image_pkl_raw:  # Pickle data is binary, so rb
                image_pkl, color_mapping = pickle.load(image_pkl_raw)

            # Sets values for color mapping
            self.image = image_pkl
            self.color_mapping = color_mapping
            self.is_RGB = False

        # Wrong file type raises error
        else:
            raise ValueError("Image contains unsupported extension")

    def save(self, filepath):
        # Check if image is present
        if self.image is None:
            raise ValueError("No image loaded")

        # Add .png extension if RGB image doesn't have it
        if self.is_RGB:
            if not filepath.endswith(".png"):
                path = filepath + ".png"
            else:
                path = filepath
            image = Image.fromarray(self.image)  # Creates a PIL Image-objet
            image.save(path)  # Saves image to disk as "path"

        # Add .pkl extension if colormap image doens't have it
        else:
            if not filepath.endswith(".pkl"):
                path = filepath + ".pkl"
            else:
                path = filepath

            with open(path, "wb") as file:  # Storing in pickle is in binary, so wb
                pickle.dump((self.image, self.color_mapping), file)  # Stores both inside file

    def change_image_format(self, format, bins=2):
        if self.image is None:
            raise ValueError("No loaded image")

        # Nothing to change
        if format == self.is_RGB:
            return

        # RGB → COLORMAP
        if (format is False) and (self.is_RGB is True):

            img = self.image.astype(np.float64) / 255.0
            h, w, _ = img.shape

            # Compute bins per channel
            r_bin = np.clip((img[:, :, 0] * bins).astype(int), 0, bins - 1)
            g_bin = np.clip((img[:, :, 1] * bins).astype(int), 0, bins - 1)
            b_bin = np.clip((img[:, :, 2] * bins).astype(int), 0, bins - 1)

            # *** Correct order: B fastest, then G, then R ***
            group_id = b_bin + g_bin * bins + r_bin * bins * bins

            flat_groups = group_id.reshape(-1)
            flat_pixels = img.reshape(-1, 3)

            # Unique sorted group IDs
            unique_groups, inverse = np.unique(flat_groups, return_inverse=True)

            # Map old group ids → new compact 0..N-1 ids
            new_ids = inverse.reshape(h, w)

            # pick correct dtype
            max_id = len(unique_groups) - 1
            if max_id < 256:
                new_ids = new_ids.astype(np.uint8)
            else:
                new_ids = new_ids.astype(np.uint16)

            # Build color map
            color_map = {}
            for new_id in range(len(unique_groups)):
                indices = np.where(inverse == new_id)[0]
                mean_color = flat_pixels[indices].mean(axis=0)
                color_map[new_id] = mean_color

            self.image = new_ids
            self.color_mapping = color_map
            self.is_RGB = False
            return

        # Color map → RGB
        if (format is True) and (self.is_RGB is False):
            ids = self.image
            h, w = ids.shape
            rgb = np.zeros((h, w, 3), dtype=np.uint8)

            for k, v in self.color_mapping.items():
                col = (v * 255).astype(np.uint8)
                mask = (ids == k)
                rgb[mask] = col

            self.image = rgb
            self.color_mapping = None
            self.is_RGB = True

    def rotate_colors(self):
        """
        - Geen image geladen  -> ValueError
        - RGB-mode            -> roteer kanalen: (R,G,B) -> (G,B,R)
        - colormap-mode       -> roteer kleuren over IDs: ID k krijgt de kleur van ID k-1
        """
        if self.image is None:
            raise ValueError("No image loaded")

        if self.is_RGB:
            # RGB: roteer de drie kanalen
            r = self.image[:, :, 0].copy()
            g = self.image[:, :, 1].copy()
            b = self.image[:, :, 2].copy()
            # (R,G,B) -> (G,B,R)
            self.image[:, :, 0] = g
            self.image[:, :, 1] = b
            self.image[:, :, 2] = r
        else:
            # colormap: roteer de kleuren over de IDs
            if self.color_mapping is None:
                raise ValueError("No color map")

            # deepcopy, zodat we vanuit de oude colormap lezen
            old = copy.deepcopy(self.color_mapping)

            # we gaan ervan uit dat keys 0..N-1 zijn, in volgorde
            keys = sorted(old.keys())
            n = len(keys)

            # ID (k+1) krijgt de oude kleur van ID
            for k in keys:
                self.color_mapping[(k + 1) % n] = old[k]

    def blur_RGB_images(self, size=3):
        if self.image is None:
            raise ValueError("No loaded image")
        if not self.is_RGB:
            return  # Not possible for a Color map

        h, w, _ = self.image.shape
        blurred = np.zeros_like(self.image)
        half = size // 2

        for i in range(h):
            for j in range(w):
                r1 = max(0, i - half)
                r2 = min(h, i + half + 1)
                c1 = max(0, j - half)
                c2 = min(w, j + half + 1)

                region = self.image[r1:r2, c1:c2]
                blurred[i, j] = region.mean(axis=(0, 1))

        self.image = blurred

    def pixelate_images(self, area, size=10):
        if self.image is None:
            raise ValueError("No loaded image")

        (xmin, xmax), (ymin, ymax) = area

        h, w = self.image.shape[:2]

        # Setting min and max values
        xmin = max(0, xmin)
        ymin = max(0, ymin)
        xmax = min(w, xmax)
        ymax = min(h, ymax)

        for y in range(ymin, ymax, size):
            for x in range(xmin, xmax, size):
                r1 = y
                r2 = min(y + size, ymax)
                c1 = x
                c2 = min(x + size, xmax)

                block = self.image[r1:r2, c1:c2]

                if self.is_RGB:
                    mean_color = block.mean(axis=(0, 1))
                    self.image[r1:r2, c1:c2] = mean_color
                else:
                    flat = block.reshape(-1)
                    counts = np.bincount(flat)
                    mode_id = counts.argmax()
                    self.image[r1:r2, c1:c2] = mode_id

    def show(self, filename=None):
        """
        This shows the images or saves the image if an filename is given.
        This works for both image formats.
        """
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

    # Pumpkin area
    area = ((0, img.shape()[1]), (0, img.shape()[0]))

    # Pixelate only the pumpkin
    img.pixelate_images(area, size=10)

    # Save result
    img.save("pumpkin_masked.png")
