# Generated by Django 3.2.3 on 2025-03-22 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DogKennelGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название группы вольеров', max_length=64, unique=True, verbose_name='Название группы вольеров')),
            ],
            options={
                'verbose_name': 'Группа вольеров',
                'verbose_name_plural': 'Группы вольеров',
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Имя', max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Фамилия', max_length=64, verbose_name='Фамилия')),
            ],
            options={
                'verbose_name': 'Владелец',
                'verbose_name_plural': 'Владельцы',
            },
        ),
        migrations.CreateModel(
            name='DogInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Имя животного', max_length=64, verbose_name='Имя')),
                ('color', models.CharField(help_text='Окрас животного', max_length=128, verbose_name='Окрас')),
                ('gender', models.CharField(choices=[('M', 'Мальчик'), ('F', 'Девочка')], default='M', help_text='Пол животного', max_length=1, verbose_name='Пол')),
                ('is_neutered', models.BooleanField(default=False, help_text='Кастрировано? Да/Нет(по умолчанию)', verbose_name='Кастрация')),
                ('description', models.TextField(blank=True, help_text='Описание животного', verbose_name='Описание')),
                ('notes', models.TextField(blank=True, help_text='Дополнительные примечания', null=True, verbose_name='Примечания')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dogs', to='database.owner')),
            ],
            options={
                'verbose_name': 'Собака',
                'verbose_name_plural': 'Собаки',
            },
        ),
        migrations.CreateModel(
            name='DogHealthIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chronic_diseases', models.TextField(blank=True, help_text='Хронические заболевания (необязательный пункт)', null=True, verbose_name='Хронические заболевания')),
                ('treatment', models.TextField(blank=True, help_text='Назначенное лечение (необязательное поле)', null=True, verbose_name='Назначенное лечение')),
                ('notes', models.TextField(blank=True, help_text='Дополнительные примечания', null=True, verbose_name='Примечания')),
                ('dog', models.OneToOneField(help_text='ID собаки', on_delete=django.db.models.deletion.CASCADE, to='database.doginfo', verbose_name='ID собаки')),
            ],
            options={
                'verbose_name': 'Здоровье собаки',
                'verbose_name_plural': 'Здоровье собак',
            },
        ),
        migrations.CreateModel(
            name='DogDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(help_text='Ориентировочная дата рождения (с точностью до года, если что, ставим 1 января соответствующего года)', verbose_name='Дата рождения')),
                ('intake_date', models.DateField(help_text='Ориентировочная дата заселения в приют (с точностью до года, если что, ставим 1 января соответствующего года)', verbose_name='Дата заселения в приют')),
                ('is_at_shelter', models.BooleanField(default=True, help_text='Находится в приюте? Да(по умолчанию)/Нет', verbose_name='Находится в приюте')),
                ('outtake_date', models.DateField(blank=True, help_text='Дата убытия из приюта', null=True, verbose_name='Дата убытия из приюта')),
                ('outtake_reasons', models.TextField(blank=True, help_text='Причина убытия', null=True, verbose_name='Причина убытия')),
                ('intake_place', models.TextField(blank=True, help_text='Откуда животное попало в приют?', null=True, verbose_name='Место изъятия')),
                ('notes', models.TextField(blank=True, help_text='Дополнительные примечания', null=True, verbose_name='Примечания')),
                ('dog', models.OneToOneField(help_text='ID собаки', on_delete=django.db.models.deletion.CASCADE, to='database.doginfo', verbose_name='ID собаки')),
            ],
            options={
                'verbose_name': 'Даты (собаки)',
                'verbose_name_plural': 'Даты (собаки)',
            },
        ),
        migrations.CreateModel(
            name='CatInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Имя животного', max_length=64, verbose_name='Имя')),
                ('color', models.CharField(help_text='Окрас животного', max_length=128, verbose_name='Окрас')),
                ('gender', models.CharField(choices=[('M', 'Мальчик'), ('F', 'Девочка')], default='M', help_text='Пол животного', max_length=1, verbose_name='Пол')),
                ('is_neutered', models.BooleanField(default=False, help_text='Кастрировано? Да/Нет(по умолчанию)', verbose_name='Кастрация')),
                ('description', models.TextField(blank=True, help_text='Описание животного', verbose_name='Описание')),
                ('notes', models.TextField(blank=True, help_text='Дополнительные примечания', null=True, verbose_name='Примечания')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cats', to='database.owner')),
            ],
            options={
                'verbose_name': 'Кошка',
                'verbose_name_plural': 'Кошки',
            },
        ),
        migrations.CreateModel(
            name='CatHealthIssues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chronic_diseases', models.TextField(blank=True, help_text='Хронические заболевания (необязательный пункт)', null=True, verbose_name='Хронические заболевания')),
                ('treatment', models.TextField(blank=True, help_text='Назначенное лечение (необязательное поле)', null=True, verbose_name='Назначенное лечение')),
                ('notes', models.TextField(blank=True, help_text='Дополнительные примечания', null=True, verbose_name='Примечания')),
                ('felv_status', models.CharField(choices=[('Y', 'Положительно'), ('N', 'Отрицательно'), ('U', 'Неизвестно')], default='U', help_text='Лейкоз у кисы: да(по умолчанию)/нет', max_length=1, verbose_name='Вирус лейкоза кошек')),
                ('fiv_status', models.CharField(choices=[('Y', 'Положительно'), ('N', 'Отрицательно'), ('U', 'Неизвестно')], default='U', help_text='Иммунодефицит у кисы: да(по умолчанию)/нет', max_length=1, verbose_name='Иммунодефицит')),
                ('cat', models.OneToOneField(help_text='ID кошки', on_delete=django.db.models.deletion.CASCADE, to='database.catinfo', verbose_name='ID кошки')),
            ],
            options={
                'verbose_name': 'Здоровье кошки',
                'verbose_name_plural': 'Здоровье кошек',
            },
        ),
        migrations.CreateModel(
            name='CatDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(help_text='Ориентировочная дата рождения (с точностью до года, если что, ставим 1 января соответствующего года)', verbose_name='Дата рождения')),
                ('intake_date', models.DateField(help_text='Ориентировочная дата заселения в приют (с точностью до года, если что, ставим 1 января соответствующего года)', verbose_name='Дата заселения в приют')),
                ('is_at_shelter', models.BooleanField(default=True, help_text='Находится в приюте? Да(по умолчанию)/Нет', verbose_name='Находится в приюте')),
                ('outtake_date', models.DateField(blank=True, help_text='Дата убытия из приюта', null=True, verbose_name='Дата убытия из приюта')),
                ('outtake_reasons', models.TextField(blank=True, help_text='Причина убытия', null=True, verbose_name='Причина убытия')),
                ('intake_place', models.TextField(blank=True, help_text='Откуда животное попало в приют?', null=True, verbose_name='Место изъятия')),
                ('notes', models.TextField(blank=True, help_text='Дополнительные примечания', null=True, verbose_name='Примечания')),
                ('cat', models.OneToOneField(help_text='ID кошки', on_delete=django.db.models.deletion.CASCADE, to='database.catinfo', verbose_name='ID кошки')),
            ],
            options={
                'verbose_name': 'Даты (кошки)',
                'verbose_name_plural': 'Даты (кошки)',
            },
        ),
        migrations.CreateModel(
            name='DogKennel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dog_kennel', to='database.dogkennelgroup')),
            ],
            options={
                'verbose_name': 'Вольер',
                'verbose_name_plural': 'Вольеры',
                'unique_together': {('group', 'name')},
            },
        ),
    ]
