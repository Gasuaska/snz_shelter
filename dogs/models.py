import os

from datetime import date, datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from taggit.managers import TaggableManager

from database.constants import KENNEL_CHOICES
from database.models import BaseHealthInfo, BaseInfoModel, Owner


class DogInfo(BaseInfoModel):
    LOWER = 'Low'
    MIDDLE = 'Mid'
    HIGHER = 'High'

    HEIGHT_CHOICES = [
        (LOWER, 'ниже колена'),
        (MIDDLE, 'по колено'),
        (HIGHER, 'выше колена'),
    ]

    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец',
        related_name='dogs'
    )
    kennel = models.CharField(
        max_length=64,
        choices=KENNEL_CHOICES,
        default=None,
        help_text='Вольер',
        verbose_name='Вольер',
        blank=True,
        null=True
        )

    height = models.CharField(
        max_length=4,
        choices=HEIGHT_CHOICES,
        default=MIDDLE,
        verbose_name='Рост собаки'
    )
    tags = TaggableManager(blank=True, verbose_name='Теги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'

    @property
    def height_display(self):
        return dict(self.HEIGHT_CHOICES).get(self.height, 'Не указано')



class DogHealth(BaseHealthInfo):
    dog = models.OneToOneField(
        DogInfo,
        on_delete=models.CASCADE,
        related_name='dog_health'
    )
    class Meta:
        verbose_name = 'Здоровье собаки'
        verbose_name_plural = 'Здоровье собак'

    def __str__(self):
        return self.dog.name


class DogDescription(models.Model):
    dog = models.OneToOneField(
        DogInfo,
        on_delete=models.CASCADE,
        related_name='dog_description'
    )
    bio = models.TextField(
        help_text='История появления животного в приюте',
        verbose_name='Биография'
    )
    character = models.TextField(
        help_text='Характер животного',
        verbose_name='Характер'
    )
    best_owner = models.TextField(
        null=True,
        blank=True,
        help_text='Кому подойдет (необязательное поле)',
        verbose_name='Лучшие владельцы для животного'
    )

    class Meta:
        verbose_name = 'Описание собаки'
        verbose_name_plural = 'Описания собак'

    def __str__(self):
        return self.dog.name


@receiver(post_save, sender=DogInfo)
def create_dog_description(sender, instance, created, **kwargs):
    if created:
        DogDescription.objects.create(
            dog=instance,
            bio='',
            character='',
            best_owner=''
        )


def dog_image_upload_to(instance, filename):
    dog_id = instance.animal.id
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    return f'dogs/{dog_id}/{date_str}{ext}'


class DogPhoto(models.Model):
    image = models.ImageField(
        upload_to=dog_image_upload_to,
        verbose_name='Фотография'
    )
    animal = models.ForeignKey(
        'DogInfo',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Животное'
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name='Основная фотография'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Фотография собаки'
        verbose_name_plural = 'Фотографии собак'


    def __str__(self):
        return f'{self.animal}-{self.uploaded_at} {self.is_main}'

    @property
    def main_photo(self):
        return self.photos.filter(is_main=True).first()

