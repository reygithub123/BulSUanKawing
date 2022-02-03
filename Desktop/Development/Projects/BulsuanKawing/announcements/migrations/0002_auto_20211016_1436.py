# Generated by Django 3.2.7 on 2021-10-16 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20211016_0924'),
        ('images', '0002_auto_20211016_1355'),
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='img_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.imagecollection'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='src_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization'),
        ),
    ]
