# Generated by Django 3.2 on 2021-05-27 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0153_genericerror_fields'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='lottransaction',
            index=models.Index(fields=['delivery_status'], name='transaction_deliver_6b302e_idx'),
        ),
        migrations.AddIndex(
            model_name='lotv2',
            index=models.Index(fields=['period'], name='lots_v2_period_a58f40_idx'),
        ),
    ]
