# Generated by Django 3.2.7 on 2021-11-21 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office_name', models.CharField(max_length=100, unique=True)),
                ('about', models.TextField(default='About BulSU-OSOA')),
                ('description', models.TextField(default='What is BulSU-OSOA?')),
                ('history', models.TextField(default='BulSU-OSOA Complete History')),
                ('logo', models.ImageField(default='osologo.svg', upload_to='imageresources/')),
            ],
        ),
        migrations.CreateModel(
            name='Officers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('image', models.ImageField(default='osologo.svg', upload_to='exectiveboard/')),
            ],
        ),
    ]
