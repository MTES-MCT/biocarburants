# Generated by Django 3.0.7 on 2020-08-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_pays_name_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='producer_with_mac',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entity',
            name='producer_with_trading',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entity',
            name='trading_certificate',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
