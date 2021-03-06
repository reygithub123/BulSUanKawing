# Generated by Django 3.2.7 on 2021-10-27 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0008_alter_imagecollection_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagecollection',
            options={'verbose_name_plural': 'Image Collection'},
        ),
        migrations.AddField(
            model_name='imagecollection',
            name='uploaded',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='imagecollection',
            name='img_src',
            field=models.FileField(upload_to='images/imageresources/'),
        ),
    ]
