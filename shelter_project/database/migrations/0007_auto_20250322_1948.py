# Generated by Django 3.2.3 on 2025-03-22 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20250322_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='address',
            field=models.CharField(blank=True, help_text='Адрес владельца', max_length=128, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='owner',
            name='phone_number',
            field=models.CharField(blank=True, help_text='Номер телефона', max_length=64, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AddField(
            model_name='owner',
            name='surname',
            field=models.CharField(blank=True, help_text='Отчество', max_length=128, null=True, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='cathealth',
            name='felv_status',
            field=models.CharField(choices=[('Y', 'Положительно'), ('N', 'Отрицательно'), ('U', 'Неизвестно')], default='U', help_text='Лейкоз у кисы: да/нет/неизвестно(по умолчанию)', max_length=1, verbose_name='Вирус лейкоза кошек'),
        ),
        migrations.AlterField(
            model_name='cathealth',
            name='fiv_status',
            field=models.CharField(choices=[('Y', 'Положительно'), ('N', 'Отрицательно'), ('U', 'Неизвестно')], default='U', help_text='Иммунодефицит у кисы: да/нет/неизвестно(по умолчанию)', max_length=1, verbose_name='Иммунодефицит'),
        ),
    ]
