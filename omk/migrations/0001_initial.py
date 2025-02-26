# Generated by Django 5.1.6 on 2025-02-26 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_type', models.CharField(choices=[('percent', 'Percent'), ('fixed', 'Fixed')], default='percent', max_length=10)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('usage_limit', models.PositiveIntegerField(default=1)),
                ('used_count', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('event', models.ForeignKey(help_text='Event terkait voucher ini.', on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='omk.event')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(help_text='Nomor telepon customer.', max_length=20)),
                ('firstLocation', models.CharField(max_length=100)),
                ('lastLocation', models.CharField(max_length=100)),
                ('messages', models.TextField(blank=True, max_length=500)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=10)),
                ('discount_applied', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(help_text='Event terkait order ini.', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='omk.event')),
                ('voucher', models.ForeignKey(blank=True, help_text='Voucher yang digunakan pada order ini.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='omk.voucher')),
            ],
        ),
    ]
