# Generated by Django 5.1.2 on 2024-10-16 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libri', '0002_alter_libri_data_pubblicazione'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libri',
            name='data_pubblicazione',
        ),
        migrations.AddField(
            model_name='libri',
            name='anno_pubblicazione',
            field=models.CharField(default=2000, max_length=10, verbose_name='Anno di pubblicazione'),
            preserve_default=False,
        ),
    ]
