# Generated by Django 3.2.7 on 2021-10-17 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0008_auto_20211017_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcollection',
            name='category',
            field=models.CharField(default='Event Registration', max_length=50),
        ),
    ]