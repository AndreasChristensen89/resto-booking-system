# Generated by Django 3.2.8 on 2021-11-22 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0009_alter_booking_booking_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_end',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_start',
            field=models.DateTimeField(),
        ),
    ]
