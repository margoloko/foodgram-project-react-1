# Generated by Django 3.2.15 on 2022-08-09 14:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220809_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountingredients',
            name='amount',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1, message='Введите количество больше 0.')], verbose_name='Количество'),
        ),
    ]
