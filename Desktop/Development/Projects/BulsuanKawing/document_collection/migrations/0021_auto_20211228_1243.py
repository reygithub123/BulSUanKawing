# Generated by Django 3.2.7 on 2021-12-28 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0020_auto_20211228_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='doc_type',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
