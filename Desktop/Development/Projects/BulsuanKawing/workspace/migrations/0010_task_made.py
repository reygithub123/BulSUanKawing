# Generated by Django 3.2.7 on 2021-12-12 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0009_auto_20211017_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='made',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
