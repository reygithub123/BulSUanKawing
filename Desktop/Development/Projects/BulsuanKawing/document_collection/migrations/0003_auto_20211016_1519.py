# Generated by Django 3.2.7 on 2021-10-16 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0002_auto_20211016_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='documentcollection',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
