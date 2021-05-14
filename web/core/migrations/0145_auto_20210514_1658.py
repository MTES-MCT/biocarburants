# Generated by Django 3.2 on 2021-05-14 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0144_auto_20210514_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lotvalidationerror',
            name='lot',
        ),
        migrations.RemoveField(
            model_name='lotvalidationerror',
            name='tx',
        ),
        migrations.RemoveField(
            model_name='transactionerror',
            name='tx',
        ),
        migrations.DeleteModel(
            name='LotV2Error',
        ),
        migrations.DeleteModel(
            name='LotValidationError',
        ),
        migrations.DeleteModel(
            name='TransactionError',
        ),
    ]