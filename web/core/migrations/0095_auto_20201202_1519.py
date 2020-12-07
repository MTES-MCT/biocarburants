# Generated by Django 3.0.7 on 2020-12-02 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0094_auto_20201201_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depot',
            name='ownership_type',
        ),
        migrations.AlterField(
            model_name='lottransaction',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tx_lot', to='core.LotV2'),
        ),
        migrations.CreateModel(
            name='OperatorDepot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ownership_type', models.CharField(choices=[('OWN', 'Propre'), ('THIRD_PARTY', 'Tiers')], default='THIRD_PARTY', max_length=32)),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Depot')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Entity')),
            ],
            options={
                'verbose_name': 'Dépôt Opérateur',
                'verbose_name_plural': 'Dépôts Opérateur',
                'db_table': 'operator_depot',
            },
        ),
    ]