# Generated by Django 3.2 on 2021-04-17 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('film_base', '0011_vsession_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VSession',
            new_name='Session',
        ),
    ]
