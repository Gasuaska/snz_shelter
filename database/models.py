from django.utils import timezone
from django.db import models
from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import TaggableManager


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


class AnimalTag(TagBase):
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Описание тега',
        verbose_name='Описание тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class TaggedAnimal(GenericTaggedItemBase):
    tag = models.ForeignKey(
        AnimalTag,
        on_delete=models.CASCADE,
        related_name='tagged_items',
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Животное с тегом'
        verbose_name_plural = 'Животные с тегами'


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
    tags = TaggableManager(
        through=TaggedAnimal,
        blank=True
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
