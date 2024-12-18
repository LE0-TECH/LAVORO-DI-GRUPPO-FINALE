# Generated by Django 5.1.2 on 2024-10-15 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Libri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=200, verbose_name='Titolo')),
                ('autore', models.CharField(max_length=100, verbose_name='Autore')),
                ('genere', models.CharField(blank=True, max_length=50, null=True, verbose_name='Genere')),
                ('data_pubblicazione', models.DateField(verbose_name='Data di pubblicazione')),
            ],
        ),
    ]
