from django.db import models

from django.contrib.auth.models import User


class Staff(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=64)
    last_name = models.CharField(verbose_name='Фамилия', max_length=64)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Year(models.Model):
    title = models.IntegerField(verbose_name='Год')
    staff = models.ForeignKey(Staff, verbose_name='Сотрудник', on_delete=models.CASCADE, related_name='year')


class Month(models.Model):
    title = models.CharField(verbose_name='Название', max_length=15)
    year = models.ForeignKey(Year, verbose_name='Отчет', on_delete=models.CASCADE, related_name='month')

    def __str__(self):
        return ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'][int(self.title) - 1]


class BigReportStaff(models.Model):
    first_year = models.IntegerField(verbose_name='С года')
    first_month = models.IntegerField(verbose_name='С месяца')
    last_year = models.IntegerField(verbose_name='По год')
    last_month = models.IntegerField(verbose_name='По месяц')

    staff = models.ForeignKey(Staff, verbose_name='Cотрудник', related_name='BigReportStaff', null=True, on_delete=models.CASCADE)


class Criteria(models.Model):
    title = models.CharField(verbose_name='Название', max_length=256)
    value = models.FloatField(verbose_name='Значение', null=True)

    month = models.ForeignKey(Month,               verbose_name='Месяц',                        on_delete=models.CASCADE, related_name='criteria', null=True)
    big_report = models.ForeignKey(BigReportStaff, verbose_name='Большой репорт по сотруднику', on_delete=models.CASCADE, related_name='criteria', null=True)

    create_date = models.DateField(verbose_name='Дата создания', auto_now=True)


class IntegralYear(models.Model):
    title = models.IntegerField(verbose_name='Год')

    economy_effectiveness = models.FloatField(verbose_name='Экономическая эффективность', null=True)
    value_product = models.FloatField(verbose_name='Объём реализованной продукции')
    fond_zp = models.FloatField(verbose_name='Фонд заработной платы')
    average_annual_value_capital = models.FloatField(verbose_name='Среднегодовая стоимость оборотных средств')
    average_annual_value_fond = models.FloatField(verbose_name='Среднегодовая стоимость основных фондов')

    soc_effectiveness = models.FloatField(verbose_name='Социальная эффективность', null=True)
    w = models.FloatField(verbose_name='Выработка')
    average_zp = models.FloatField(verbose_name='Среднегодовая заработная плата одного работника')

    financial_efficiency = models.FloatField(verbose_name='Финансовая эффективность', null=True)
    profit_before_tax = models.FloatField(verbose_name='Прибыль до налогообложения')

    indicators_of_the_use_resources = models.FloatField(verbose_name='Интегральный показатель эффективности хозяйственной деятельности', null=True)
