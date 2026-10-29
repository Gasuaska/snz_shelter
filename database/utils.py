from io import BytesIO
import base64

import qrcode
from django.core.files.base import ContentFile
from PIL import Image, ImageOps
from django.urls import reverse

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

def make_dog_qr(dog):
    path = reverse('dogs:dog_detail', args=[dog.pk])
    url = f'https://drugizpriyuta.ru{path}'

    image = qrcode.make(url)

    buffer = BytesIO()
    image.save(buffer, format='PNG')

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode('ascii')

    return f'data:image/png;base64,{encoded}'


def prepare_dog_card(dog):
    main_photo = dog.photos.filter(is_main=True).first()

    if main_photo is None:
        main_photo = dog.photos.first()

    return {
        'dog': dog,
        'main_photo': main_photo,
        'qr_code': make_dog_qr(dog),
    }
