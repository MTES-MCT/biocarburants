# Generated by Django 3.0.7 on 2020-11-03 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_auto_20201028_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='lottransaction',
            name='is_batch',
            field=models.BooleanField(default=False),
        ),
    ]