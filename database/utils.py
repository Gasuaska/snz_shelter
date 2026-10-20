from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

def generate_thumbnail(file):
    img = Image.open(file)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((400, 400))
    img = img.convert('RGBA')
    background = Image.new('RGB', img.size, 'white')
    background.paste(img, mask=img.getchannel('A'))
    img = background
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    return ContentFile(buffer.getvalue())