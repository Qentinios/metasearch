# Generated by Django 3.1.6 on 2021-06-07 00:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20210603_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cena'),
        ),
    ]
