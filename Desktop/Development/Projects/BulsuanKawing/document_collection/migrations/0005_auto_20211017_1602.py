# Generated by Django 2.0.7 on 2021-10-17 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0004_auto_20211017_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentcollection',
            name='date_submitted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
