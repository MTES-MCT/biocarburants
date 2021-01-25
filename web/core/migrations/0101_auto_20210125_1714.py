# Generated by Django 3.0.7 on 2021-01-25 16:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0100_auto_20210120_1326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sustainabilitydeclaration',
            name='month',
        ),
        migrations.RemoveField(
            model_name='sustainabilitydeclaration',
            name='year',
        ),
        migrations.AddField(
            model_name='sustainabilitydeclaration',
            name='deadline',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='sustainabilitydeclaration',
            name='period',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
    ]
