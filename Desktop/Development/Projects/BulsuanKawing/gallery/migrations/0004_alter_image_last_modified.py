# Generated by Django 3.2.7 on 2021-11-30 10:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20211128_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
