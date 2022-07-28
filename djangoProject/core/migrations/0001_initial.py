# Generated by Django 3.2.11 on 2022-05-29 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BigReportStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_year', models.IntegerField(verbose_name='С года')),
                ('first_month', models.IntegerField(verbose_name='С месяца')),
                ('last_year', models.IntegerField(verbose_name='По год')),
                ('last_month', models.IntegerField(verbose_name='По месяц')),
            ],
        ),
        migrations.CreateModel(
            name='IntegralYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.IntegerField(verbose_name='Год')),
                ('economy_effectiveness', models.FloatField(null=True, verbose_name='Экономическая эффективность')),
                ('value_product', models.FloatField(verbose_name='Объём реализованной продукции')),
                ('fond_zp', models.FloatField(verbose_name='Фонд заработной платы')),
                ('average_annual_value_capital', models.FloatField(verbose_name='Среднегодовая стоимость оборотных средств')),
                ('average_annual_value_fond', models.FloatField(verbose_name='Среднегодовая стоимость основных фондов')),
                ('soc_effectiveness', models.FloatField(null=True, verbose_name='Социальная эффективность')),
                ('w', models.FloatField(verbose_name='Выработка')),
                ('average_zp', models.FloatField(verbose_name='Среднегодовая заработная плата одного работника')),
                ('financial_efficiency', models.FloatField(null=True, verbose_name='Финансовая эффективность')),
                ('profit_before_tax', models.FloatField(verbose_name='Прибыль до налогообложения')),
                ('indicators_of_the_use_resources', models.FloatField(null=True, verbose_name='Интегральный показатель эффективности хозяйственной деятельности')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=64, verbose_name='Фамилия')),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.IntegerField(verbose_name='Год')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='year', to='core.staff', verbose_name='Сотрудник')),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15, verbose_name='Название')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='month', to='core.year', verbose_name='Отчет')),
            ],
        ),
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('value', models.FloatField(null=True, verbose_name='Значение')),
                ('create_date', models.DateField(auto_now=True, verbose_name='Дата создания')),
                ('big_report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='criteria', to='core.bigreportstaff', verbose_name='Большой репорт по сотруднику')),
                ('month', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='criteria', to='core.month', verbose_name='Месяц')),
            ],
        ),
        migrations.AddField(
            model_name='bigreportstaff',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BigReportStaff', to='core.staff', verbose_name='Cотрудник'),
        ),
    ]