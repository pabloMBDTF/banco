# Generated by Django 4.1.4 on 2023-01-04 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bancoapp', '0003_fondobanco_remove_fondo_total'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FondoBanco',
        ),
    ]
