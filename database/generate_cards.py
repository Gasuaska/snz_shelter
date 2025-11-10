import os
from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from .models import DogInfo


def get_main_photo_path(dog: DogInfo):
    photo = dog.photos.filter(is_main=True).first() or dog.photos.first()
    if not photo:
        return None
    try:
        return photo.image.path
    except Exception:
        from django.conf import settings
        if hasattr(photo.image, 'name') and settings.MEDIA_ROOT:
            return os.path.join(settings.MEDIA_ROOT, photo.image.name)
    return None


def draw_card(c, x, y, w, h, dog: DogInfo):
    padding = 6 * mm
    c.rect(x, y, w, h)
    img_h = h * 0.6
    img_w = w - 2 * padding
    img_x = x + padding
    img_y = y + h - padding - img_h

    img_path = get_main_photo_path(dog)
    if img_path and os.path.exists(img_path):
        img = ImageReader(img_path)
        orig_w, orig_h = img.getSize()
        scale = min(img_w / orig_w, img_h / orig_h)
        draw_w = orig_w * scale
        draw_h = orig_h * scale
        draw_x = img_x + (img_w - draw_w) / 2
        draw_y = img_y + (img_h - draw_h) / 2
        c.drawImage(img, draw_x, draw_y, draw_w, draw_h, preserveAspectRatio=True)
    else:
        c.setFont("Helvetica", 10)
        c.drawCentredString(x + w / 2, img_y + img_h / 2, "Фото отсутствует")

    # текст под картинкой
    text_y = img_y - 10 * mm
    name_text = dog.name or "Без имени"
    dob_text = "Дата рождения: "
    if dog.birth_date:
        dob_text += dog.birth_date.strftime("%d.%m.%Y")
    else:
        dob_text += "Не указана"

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(x + w / 2, text_y + 8 * mm, name_text)
    c.setFont("Helvetica", 10)
    c.drawCentredString(x + w / 2, text_y + 3 * mm, dob_text)