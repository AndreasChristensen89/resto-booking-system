# Generated by Django 3.2.9 on 2022-01-03 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0011_auto_20211216_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='moveable',
        ),
    ]
