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

# Абстрактные модели


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
    description = models.TextField(
        null=True,
        blank=True,
        help_text='Описание животного',
        verbose_name='Описание',
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
        help_text='Назначенное лечение (необязательное поле)',
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'


class DogHealth(BaseHealthInfo):
    dog = models.ForeignKey(
        DogInfo,
        on_delete=models.CASCADE,
        related_name="dohhealth"
    )

    class Meta:
        verbose_name = 'Здоровье собаки'
        verbose_name_plural = 'Здоровье собак'

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
