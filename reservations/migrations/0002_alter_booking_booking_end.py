# Generated by Django 3.2.9 on 2021-12-07 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_end',
            field=models.DateTimeField(blank=True),
        ),
    ]
