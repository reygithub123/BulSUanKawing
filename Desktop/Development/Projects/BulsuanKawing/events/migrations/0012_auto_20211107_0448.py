# Generated by Django 3.2.7 on 2021-11-06 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_remove_event_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='state',
            field=models.CharField(blank=True, default='Pending', max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='EventState',
        ),
    ]
