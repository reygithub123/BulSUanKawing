# Generated by Django 3.2.7 on 2021-10-17 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_collection', '0013_alter_documentcollection_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcollection',
            name='submitted2',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='documentcollection',
            name='submitted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
