# Generated by Django 3.0.7 on 2021-02-26 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0111_auto_20210226_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotvalidationerror',
            name='tx',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.LotTransaction'),
        ),
    ]
