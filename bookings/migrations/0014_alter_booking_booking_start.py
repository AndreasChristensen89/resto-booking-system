# Generated by Django 3.2.8 on 2021-11-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0013_auto_20211122_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_start',
            field=models.DateTimeField(blank=True),
        ),
    ]