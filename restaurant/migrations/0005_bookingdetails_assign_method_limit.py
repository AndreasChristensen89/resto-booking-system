# Generated by Django 3.2.9 on 2021-12-15 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_rename_auto_table_assign_bookingdetails_table_assign_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingdetails',
            name='assign_method_limit',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
