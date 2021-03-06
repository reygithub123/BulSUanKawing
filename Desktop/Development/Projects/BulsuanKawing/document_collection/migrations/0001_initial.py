# Generated by Django 3.2.7 on 2021-10-16 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0004_auto_20211016_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_submitted', models.DateField(auto_now=True)),
                ('src_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('source', models.CharField(max_length=50)),
                ('CLD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document_collection.documentcollection')),
            ],
        ),
    ]
