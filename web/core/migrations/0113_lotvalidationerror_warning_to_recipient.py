# Generated by Django 3.0.7 on 2021-02-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0112_lotvalidationerror_tx'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotvalidationerror',
            name='warning_to_recipient',
            field=models.BooleanField(default=False),
        ),
    ]
