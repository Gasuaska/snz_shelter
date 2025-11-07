import os

from datetime import date, datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from .constants import KENNEL_CHOICES


class Owner(models.Model):
    first_name = models.CharField(
        max_length=64,
        help_text='Имя',
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=64,
        help_text='Фамилия',
        verbose_name='Фамилия')
    surname = models.CharField(
        max_length=128,
        help_text='Отчество',
        verbose_name='Отчество',
        null=True,
        blank=True,)
    phone_number = models.CharField(
        max_length=64,
        help_text='Номер телефона',
        verbose_name='Номер телефона',
        null=True,
        blank=True,
        )
    address = models.CharField(
        max_length=128,
        help_text='Адрес владельца',
        verbose_name='Адрес',
        null=True,
        blank=True,
        )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'


class BaseInfoModel(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (MALE, 'Мальчик'),
        (FEMALE, 'Девочка'),
    ]

    name = models.CharField(
        max_length=64,
        help_text='Имя животного',
        verbose_name='Имя'
        )
    color = models.CharField(
        max_length=128,
        help_text='Окрас животного',
        verbose_name='Окрас'
        )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MALE,
        help_text='Пол животного',
        verbose_name='Пол',
        )
    is_neutered = models.BooleanField(
        default=False,
        help_text='Кастрировано? Да/Нет(по умолчанию)',
        verbose_name='Кастрация'
        )
    birth_date = models.DateField(
        help_text=('Ориентировочная дата рождения (с точностью до года,'
                   ' если что, ставим 1 января соответствующего года)'),
        verbose_name='Дата рождения'
        )
    intake_date = models.DateField(
        help_text=('Ориентировочная дата заселения в приют (с точностью до '
                   'года, если что, ставим 1 января соответствующего года)'),
        verbose_name='Дата заселения в приют',
        )
    is_at_shelter = models.BooleanField(
        default=True,
        help_text='Находится в приюте? Да(по умолчанию)/Нет',
        verbose_name='Находится в приюте'
        )
    outtake_date = models.DateField(
        null=True,
        blank=True,
        help_text='Дата убытия из приюта',
        verbose_name='Дата убытия из приюта',
        )
    outtake_reasons = models.TextField(
        null=True,
        blank=True,
        help_text='Причина убытия',
        verbose_name='Причина убытия',
    )
    intake_place = models.TextField(
        null=True,
        blank=True,
        help_text='Откуда животное попало в приют?',
        verbose_name='Место изъятия',
        )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text='Дополнительные примечания',
        verbose_name='Примечания',
        )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def age(self):
        today = timezone.now().date()
        if not self.birth_date:
            return None
        years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

    @property
    def age_display(self):
        age = self.age
        if age is None:
            return 'Неизвестен'

        if age % 10 == 1 and age % 100 != 11:
            return f'{age} год'
        elif 2 <= age % 10 <= 4 and not 12 <= age % 100 <= 14:
            return f'{age} года'
        else:
            return f'{age} лет'

    @property
    def gender_neutered_display(self):
        if self.gender == 'M':
            return 'кастрирован' if self.is_neutered else 'не кастрирован'
        return 'кастрирована' if self.is_neutered else 'не кастрирована'
 
    @property
    def gender_display(self):
        if self.gender == 'M':
            return 'мальчик'
        return 'девочка'
    
    @property
    def intake_year(self):
        if self.intake_date:
            return self.intake_date.year
        return 'Неизвестен'


class BaseHealthInfo(models.Model):
    chronic_diseases = models.TextField(
        null=True,
        blank=True,
        help_text='Хронические заболевания (необязательный пункт)',
        verbose_name='Хронические заболевания'
        )
    treatment = models.TextField(
        null=True,
        blank=True,
        help_text=('Назначенное лечение (необязательное поле), дописываем, '
                   'не удаляя старое: даты, лекарство, дозировка,'
                   'будет своеобразный архив'),
        verbose_name='Назначенное лечение'
        )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text='Дополнительные примечания',
        verbose_name='Примечания'
        )

    class Meta:
        abstract = True

# СОБАКИ


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'

    @property
    def height_display(self):
        return dict(self.HEIGHT_CHOICES).get(self.height, 'Не указано')

    def __str__(self):
        return self.name


class DogHealth(BaseHealthInfo):
    dog = models.ForeignKey(
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
    dog = models.ForeignKey(
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
# КОТИКИ


class CatInfo(BaseInfoModel):
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cats'
    )

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
    cat = models.ForeignKey(
        CatInfo,
        on_delete=models.CASCADE,
        related_name="cathealth"
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


def dog_image_upload_to(instance, filename):
    dog_id = instance.animal.id
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    return f'dogs/{dog_id}/{date_str}{ext}'


class AnimalPhoto(models.Model):
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
        return f'{self.animal}-{self.uploaded_at}{self.is_main}'

    @property
    def main_photo(self):
        return self.photos.filter(is_main=True).first()


@receiver(post_save, sender=DogInfo)
def create_dog_description(sender, instance, created, **kwargs):
    if created:
        DogDescription.objects.create(
            dog=instance,
            bio='',
            character='',
            best_owner=''
        )
