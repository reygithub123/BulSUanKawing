# Generated by Django 3.2.7 on 2022-01-03 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_event_state'),
        ('document_collection', '0022_document_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcollection',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.event'),
        ),
    ]
