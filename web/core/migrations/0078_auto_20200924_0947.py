# Generated by Django 3.0.7 on 2020-09-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_lotv2_is_valid'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='lottransaction',
            index=models.Index(fields=['carbure_vendor'], name='transaction_carbure_223649_idx'),
        ),
        migrations.AddIndex(
            model_name='lottransaction',
            index=models.Index(fields=['carbure_client'], name='transaction_carbure_81c6e1_idx'),
        ),
        migrations.AddIndex(
            model_name='lotv2',
            index=models.Index(fields=['status'], name='lots_v2_status_a68baa_idx'),
        ),
    ]
