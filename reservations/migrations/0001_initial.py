# Generated by Django 3.2.8 on 2021-12-05 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=200)),
                ('number_guests', models.PositiveIntegerField()),
                ('booking_start', models.DateTimeField()),
                ('booking_end', models.DateTimeField()),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Declined')], default=0)),
                ('comment', models.TextField(blank=True, max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_booking', to=settings.AUTH_USER_MODEL)),
                ('table', models.ManyToManyField(blank=True, related_name='booking_tables', to='reservations.Table')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
