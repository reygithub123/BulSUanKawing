# Generated by Django 3.2.7 on 2021-12-12 20:14

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0010_task_made'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='color',
            field=colorfield.fields.ColorField(default='#00546A', max_length=18, samples=None),
        ),
    ]
