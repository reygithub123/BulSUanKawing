# Generated by Django 3.2.7 on 2021-10-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0012_rename_date_submitted_documentcollection_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentcollection',
            name='submitted',
            field=models.DateField(auto_now=True),
        ),
    ]
