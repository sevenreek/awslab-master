from PIL import Image, ImageOps


class ImageProcessor():
    def __call__(self, sourcefile, destfile):
        raise NotImplementedError()


class ImageInverter(ImageProcessor):
    NAME = 'invert'

    def __call__(self, sourcefile, destfile):
        im = Image.open(sourcefile)
        im_invert = ImageOps.invert(im)
        im_invert.save(destfile)


class Grayscaler(ImageProcessor):
    NAME = 'grayscale'

    def __call__(self, sourcefile, destfile):
        im = Image.open(sourcefile)
        im.convert('LA')
        im.save(destfile)


class Thumbnailer(ImageProcessor):
    NAME = 'thumbnail'

    def __call__(self, sourcefile, destfile):
        image = Image.open(sourcefile)
        MAX_SIZE = (128, 128)
        image.thumbnail(MAX_SIZE)
        image.save(destfile)
