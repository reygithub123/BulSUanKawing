# Generated by Django 3.2.7 on 2021-12-16 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0014_alter_task_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='reminder_time',
        ),
        migrations.DeleteModel(
            name='AssignedOfficer',
        ),
        migrations.DeleteModel(
            name='Officer',
        ),
    ]