import os

from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from taggit.managers import TaggableManager
from django.urls import reverse

from database.models import BaseInfoModel, BaseHealthInfo, Owner

class CatInfo(BaseInfoModel):
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cats',
        verbose_name='Владелец'
    )
    urgent = models.BooleanField(
        verbose_name='Срочно ищет дом',
        default=False
    )
    priority = models.IntegerField(
        verbose_name='Приоритет',
        default=0,
        help_text='Чем больше — тем выше в списке'
    )
    
    def get_absolute_url(self):
        return reverse('cats:cat_detail', args=[self.pk])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кошка'
        verbose_name_plural = 'Кошки'


class CatHealth(BaseHealthInfo):
    POSITIVE = 'Y'
    NEGATIVE = 'N'
    UNKNOWN = 'U'
    VIRUS_STATUS_CHOICES = [
        (POSITIVE, 'Положительно'),
        (NEGATIVE, 'Отрицательно'),
        (UNKNOWN, 'Неизвестно')
    ]
    cat = models.OneToOneField(
        CatInfo,
        on_delete=models.CASCADE,
        related_name='cat_health'
    )
    felv_status = models.CharField(
        max_length=1,
        choices=VIRUS_STATUS_CHOICES,
        default=UNKNOWN,
        help_text='Лейкоз у кисы: да/нет/неизвестно(по умолчанию)',
        verbose_name='Вирус лейкоза кошек'
        )
    fiv_status = models.CharField(
        max_length=1,
        choices=VIRUS_STATUS_CHOICES,
        default=UNKNOWN,
        help_text='Иммунодефицит у кисы: да/нет/неизвестно(по умолчанию)',
        verbose_name='Иммунодефицит'
        )

    class Meta:
        verbose_name = 'Здоровье кошки'
        verbose_name_plural = 'Здоровье кошек'

    def __str__(self):
            return self.cat.name
 
    @receiver(post_save, sender=CatInfo)
    def create_cat_health(sender, instance, created, **kwargs):
        if created:
            CatHealth.objects.create(cat=instance)


class CatDescription(models.Model):
    cat = models.OneToOneField(
        CatInfo,
        on_delete=models.CASCADE,
        related_name='cat_description'
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
        verbose_name = 'Описание кошки'
        verbose_name_plural = 'Описания кошек'

    def __str__(self):
        return self.cat.name


@receiver(post_save, sender=CatInfo)
def create_cat_description(sender, instance, created, **kwargs):
    if created:
        CatDescription.objects.create(
            cat=instance,
            bio='',
            character='',
            best_owner=''
        )


def cat_image_upload_to(instance, filename):
    cat_id = instance.animal.id
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    return f'cats/{cat_id}/{date_str}{ext}'


class CatPhoto(models.Model):
    image = models.ImageField(
        upload_to=cat_image_upload_to,
        verbose_name='Фотография'
    )
    animal = models.ForeignKey(
        'CatInfo',
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
        verbose_name = 'Фотография кошки'
        verbose_name_plural = 'Фотографии кошек'


    def __str__(self):
        return f'{self.animal}-{self.uploaded_at}{self.is_main}'

    @property
    def main_photo(self):
        return self.photos.filter(is_main=True).first()
