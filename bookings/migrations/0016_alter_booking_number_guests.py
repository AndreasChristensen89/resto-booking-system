# Generated by Django 3.2.8 on 2021-11-23 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0015_alter_booking_number_guests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='number_guests',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]