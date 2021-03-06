# Generated by Django 3.2.7 on 2021-12-12 19:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0008_alter_officer_hierarchy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='hierarchy',
            field=models.PositiveIntegerField(choices=[(0, 'Head (Head of Office)'), (1, 'Leaders(Chairman/Vice Chairman)'), (2, 'Internal/Primary(Executive Borad/Committees)'), (3, 'External/Secondary'), (4, 'Others')], default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)]),
        ),
    ]
