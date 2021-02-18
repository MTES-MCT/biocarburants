# Generated by Django 3.0.7 on 2021-02-17 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0106_auto_20210212_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='legal_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='registered_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='registration_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='sustainability_officer',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='sustainability_officer_phone_number',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]