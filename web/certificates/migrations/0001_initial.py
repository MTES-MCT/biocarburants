# Generated by Django 3.2 on 2021-04-19 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0127_auto_20210324_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='SNCertificateCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=512)),
            ],
            options={
                'verbose_name': 'SN Category',
                'verbose_name_plural': 'SN Categories',
                'db_table': 'sn_categories',
            },
        ),
        migrations.CreateModel(
            name='SNCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_id', models.CharField(max_length=64)),
                ('certificate_holder', models.CharField(max_length=256)),
                ('valid_from', models.DateField()),
                ('valid_until', models.DateField()),
                ('download_link', models.CharField(default='', max_length=512)),
                ('scope', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificates.sncertificatecategory')),
            ],
            options={
                'verbose_name': 'SN Certificate',
                'verbose_name_plural': 'SN Certificates',
                'db_table': 'sn_certificates',
            },
        ),
        migrations.CreateModel(
            name='EntitySNTradingCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_been_updated', models.BooleanField(default=False)),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificates.sncertificate')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.entity')),
            ],
            options={
                'verbose_name': 'Certificat Système National',
                'verbose_name_plural': 'Certificats Système National',
                'db_table': 'entity_sn_certificates',
            },
        ),
    ]
