# Generated by Django 3.2.7 on 2021-10-17 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_auto_20211017_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]