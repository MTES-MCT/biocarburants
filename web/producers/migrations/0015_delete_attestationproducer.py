# Generated by Django 3.0.3 on 2020-05-07 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20200507_1209'),
        ('producers', '0014_auto_20200501_1320'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AttestationProducer',
        ),
    ]