# Generated by Django 3.2.7 on 2021-12-13 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0011_alter_todolist_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskstate',
            old_name='status',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='taskstate',
            name='TID',
        ),
        migrations.AddField(
            model_name='task',
            name='state',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='workspace.taskstate'),
        ),
    ]
