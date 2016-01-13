import numpy
from PIL import Image

SIZE_DICT = {
    "200%": 2,
    "150%": 1.5,
    "100%": 1,
    "50%": 0.5,
    "25%": 0.25
}


def open_image(path):
    """
    Open image from path, and prepare it's fft
    :param path: Path to image
    :type path: str
    :return: Image from path and its fft
    :rtype: (PIL.Image.Image)
    """
    return Image.open(path)


def resize(image, size):
    """
    Resize image by given size and make it B&W
    :param image: Path to image
    :type image: PIL.Image.Image
    :param size: Size in image should be scale
    :type size: str
    :return: Image after resize
    :rtype: PIL.Image.Image
    """
    size = SIZE_DICT[size]
    image = image.convert('L')

    x, y = image.size
    x = int(x*size)
    y = int(y*size)

    image = image.resize((x, y), Image.ANTIALIAS)

    return image


def FFT(image, fft_type="Real", size="100%"):
    """
    Calculates FFT of given image
    :param image: Image for which we want to calcualte FFT
    :type image: PIL.Image.Image
    :param fft_type: Which part of result we want to show
    :type fft_type: str
    :param size: Size in image should be scale
    :type size: str
    :return: Image after FFT
    :rtype: PIL.Image.Image
    """
    print("Calculate FFT type: " + fft_type)

    image = image.convert('L')

    I = numpy.asarray(image)

    I = numpy.fft.fft2(I)
    I = numpy.fft.fftshift(I)

    if fft_type == "Imaginary":
        I = I.imag
    elif fft_type == "Real":
        I = I.real
    elif fft_type == "Phase":
        I = numpy.angle(I, deg=True)
    elif fft_type == "Amplitude":
        I = numpy.absolute(I)
        I[I == 0] = 1
        I = 20*numpy.log(I)

    min = numpy.amin(I)
    max = numpy.amax(I)

    I = ((I - min)/(max - min)) * 255
    I = numpy.uint8(I)

    image = Image.fromarray(I, mode='L')

    return resize(image, size)
