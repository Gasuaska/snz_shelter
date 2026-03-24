from django.db import models


class MonthlyReport(models.Model):
    date = models.DateField(
        verbose_name='Месяц отчета',
        help_text='Месяц и год отчета',
    )
    income = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        verbose_name='Приход')
    expense = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        verbose_name='Расход')
    expense_details = models.TextField(
        verbose_name='Подробный расход'
    )
    donors = models.TextField(
        verbose_name='Список жертвователей'
    )

    def __str__(self):
        return self.date.strftime('%B %Y')

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'