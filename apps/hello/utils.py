from PIL import Image
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile

import sys


def resize_image(size: tuple, image):
    """
    This function changes size of image, maintaining aspect ratio
    """
    image_name = image.name
    image = Image.open(image)

    stream = BytesIO()
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(stream, format='JPEG', qulity=90)

    stream.seek(0)
    image_file = InMemoryUploadedFile(
        stream, 'ImageField', f'{image_name.split(".")}.jpeg',
        'image/jpeg', sys.getsizeof(stream), None
    )
    return image_file
