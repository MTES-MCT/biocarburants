# Generated by Django 3.0.7 on 2020-09-18 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_auto_20200916_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotvalidationerror',
            name='details',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
