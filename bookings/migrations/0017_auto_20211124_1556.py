# Generated by Django 3.2.8 on 2021-11-24 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0016_alter_booking_number_guests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='number_guests',
            field=models.PositiveIntegerField(),
        ),
    ]