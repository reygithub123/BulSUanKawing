# Generated by Django 3.2.7 on 2021-11-28 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0015_alter_organization_category'),
        ('gallery', '0002_auto_20211128_1922'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Albums',
            new_name='Album',
        ),
        migrations.RenameModel(
            old_name='Images',
            new_name='Image',
        ),
    ]
