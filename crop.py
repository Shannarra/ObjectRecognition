""""
Crops a new image of a bigger one by given command.
"""

from PIL import Image


def crop(impath, coords, loc):
    img = Image.open(impath)
    crped_image = img.crop(coords)
    crped_image.save(loc)
    crped_image.show()


if __name__ == '__main__':
    image = 'result/toCrop.jpg'
    crop(image, (108, 311, 226, 401), 'result/cropped2.jpg')
