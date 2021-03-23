# Generated by Django 3.0.7 on 2021-03-23 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0125_redcertcertificatebiomass'),
    ]

    operations = [
        migrations.AddField(
            model_name='lottransaction',
            name='is_forwarded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='depot',
            name='depot_type',
            field=models.CharField(choices=[('EFS', 'EFS'), ('EFPE', 'EFPE'), ('OIL DEPOT', 'OIL DEPOT'), ('BIOFUEL DEPOT', 'BIOFUEL DEPOT'), ('OTHER', 'Autre')], default='OTHER', max_length=32),
        ),
    ]
