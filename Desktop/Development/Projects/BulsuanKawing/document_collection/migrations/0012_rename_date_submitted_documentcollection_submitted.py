# Generated by Django 3.2.7 on 2021-10-17 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0011_documentcollection_date_submitted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentcollection',
            old_name='date_submitted',
            new_name='submitted',
        ),
    ]
