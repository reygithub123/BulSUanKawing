# Generated by Django 2.0.7 on 2021-10-16 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='documentcollection',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]