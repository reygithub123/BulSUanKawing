# Generated by Django 3.2.7 on 2021-11-06 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0017_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='documents/'),
        ),
    ]
