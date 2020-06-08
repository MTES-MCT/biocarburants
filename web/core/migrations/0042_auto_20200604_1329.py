# Generated by Django 3.0.3 on 2020-06-04 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('producers', '0015_delete_attestationproducer'),
        ('core', '0041_lot_ea_delivery_site_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='ea_delivery_site_fk',
        ),
        migrations.CreateModel(
            name='LotV2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(blank=True, default='', max_length=64)),
                ('carbure_id', models.CharField(blank=True, default='', max_length=64)),
                ('producer_is_in_carbure', models.BooleanField(default=True)),
                ('unknown_producer', models.CharField(blank=True, default='', max_length=64)),
                ('production_site_is_in_carbure', models.BooleanField(default=True)),
                ('unknown_production_site', models.CharField(blank=True, default='', max_length=64)),
                ('volume', models.IntegerField(default=0)),
                ('eec', models.FloatField(default=0.0)),
                ('el', models.FloatField(default=0.0)),
                ('ep', models.FloatField(default=0.0)),
                ('etd', models.FloatField(default=0.0)),
                ('eu', models.FloatField(default=0.0)),
                ('esca', models.FloatField(default=0.0)),
                ('eccs', models.FloatField(default=0.0)),
                ('eccr', models.FloatField(default=0.0)),
                ('eee', models.FloatField(default=0.0)),
                ('ghg_total', models.FloatField(default=0.0)),
                ('ghg_reference', models.FloatField(default=0.0)),
                ('ghg_reduction', models.FloatField(default=0.0)),
                ('client_id', models.CharField(blank=True, default='', max_length=64)),
                ('status', models.CharField(choices=[('Draft', 'Brouillon'), ('Validated', 'Validé')], default='Draft', max_length=64)),
                ('source', models.CharField(choices=[('EXCEL', 'Excel'), ('MANUAL', 'Manual')], default='Manual', max_length=32)),
                ('is_split', models.BooleanField(default=False)),
                ('biocarburant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Biocarburant')),
                ('carbure_producer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='producer_lotv2', to='core.Entity')),
                ('carbure_production_site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='producers.ProductionSite')),
                ('matiere_premiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.MatierePremiere')),
                ('parent_lot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.LotV2')),
                ('pays_origine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Pays')),
            ],
            options={
                'verbose_name': 'LotV2',
                'verbose_name_plural': 'LotsV2',
                'db_table': 'lots_v2',
            },
        ),
        migrations.CreateModel(
            name='LotTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_is_in_carbure', models.BooleanField(default=True)),
                ('unknown_vendor', models.CharField(blank=True, default='', max_length=64)),
                ('dae', models.CharField(blank=True, default='', max_length=64)),
                ('client_is_in_carbure', models.BooleanField(default=True)),
                ('unknown_client', models.CharField(blank=True, default='', max_length=64)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('delivery_site_is_in_carbure', models.BooleanField(default=True)),
                ('undelivery_site', models.CharField(blank=True, default='', max_length=64)),
                ('export_ue', models.BooleanField(default=False)),
                ('export_hors_ue', models.BooleanField(default=False)),
                ('delivery_status', models.CharField(choices=[('N', 'En Attente'), ('A', 'Accepté'), ('R', 'Refusé'), ('AC', 'À corriger'), ('AA', 'Corrigé')], default='N', max_length=64)),
                ('etd_impact', models.FloatField(default=0.0)),
                ('ghg_total', models.FloatField(default=0.0)),
                ('ghg_reduction', models.FloatField(default=0.0)),
                ('champ_libre', models.CharField(blank=True, default='', max_length=64)),
                ('carbure_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_transaction', to='core.Entity')),
                ('carbure_delivery_site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Depot')),
                ('carbure_vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_transaction', to='core.Entity')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.LotV2')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'transactions',
            },
        ),
    ]