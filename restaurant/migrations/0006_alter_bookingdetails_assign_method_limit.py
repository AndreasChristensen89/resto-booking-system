# Generated by Django 3.2.9 on 2021-12-15 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_bookingdetails_assign_method_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetails',
            name='assign_method_limit',
            field=models.IntegerField(blank=True, default=100),
        ),
    ]
