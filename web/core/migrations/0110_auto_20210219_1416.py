# Generated by Django 3.0.7 on 2021-02-19 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0109_auto_20210218_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depot',
            name='address',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='depot',
            name='postal_code',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]