# Generated by Django 3.2 on 2021-05-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0148_transactionupdatehistory_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionupdatehistory',
            name='value_after',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='transactionupdatehistory',
            name='value_before',
            field=models.TextField(null=True),
        ),
    ]
