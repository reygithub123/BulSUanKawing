# Generated by Django 3.2.7 on 2021-10-16 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0003_auto_20211016_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstate',
            name='status',
            field=models.CharField(default='todo', max_length=50),
        ),
    ]
