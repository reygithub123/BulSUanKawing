# Generated by Django 3.2.7 on 2021-11-06 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20211107_0448'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='state',
        ),
    ]
