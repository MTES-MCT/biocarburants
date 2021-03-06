# Generated by Django 3.0.7 on 2020-09-02 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_checkrule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='biocarburant',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='client_id',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='dae',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='ea',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='ea_delivery_date',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='ea_delivery_site',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='ea_delivery_status',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='eccr',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='eccs',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='eec',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='eee',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='el',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='ep',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='esca',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='etd',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='eu',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='ghg_reduction',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='ghg_reference',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='ghg_total',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='matiere_premiere',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='pays_origine',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='period',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='producer',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='production_site',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='status',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='volume',
        ),
    ]
