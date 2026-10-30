from uuid import uuid4
import os
from django.db import models

from database.utils import generate_thumbnail

def gallery_image_upload_to(instance, filename):
    _, ext = os.path.splitext(filename)
    return f'gallery/{uuid4().hex}{ext.lower()}'

def gallery_thumbnail_upload_to(instance, filename):
    return f'gallery/thumbnails/{filename}'


class GalleryPhoto(models.Model):
    image = models.ImageField(
        upload_to=gallery_image_upload_to,
        verbose_name='Фотография'
    )
    thumbnail = models.ImageField(
        upload_to=gallery_thumbnail_upload_to,
        blank=True,
        verbose_name='Превью'
    )
    show_in_gallery = models.BooleanField(
        default=False,
        verbose_name='Показывать в галерее'
    )
    caption = models.CharField(
        verbose_name='Подпись',
        blank=True,
        null=True,
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Фотография приюта'
        verbose_name_plural = 'Фотографии приюта'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and not self.thumbnail:
            with self.image.open('rb') as file:
                base = os.path.splitext(os.path.basename(self.image.name))[0]
                filename = f'{base}.jpg'
                thumbnail = generate_thumbnail(file)
                self.thumbnail.save(
                    filename, thumbnail, save=False)
                type(self).objects.filter(pk=self.pk).update(
                    thumbnail=self.thumbnail.name
                )
