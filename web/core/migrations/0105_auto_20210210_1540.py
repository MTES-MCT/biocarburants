# Generated by Django 3.0.7 on 2021-02-10 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0104_matierepremiere_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entity',
            name='producer_with_mac',
        ),
        migrations.RemoveField(
            model_name='entity',
            name='producer_with_trading',
        ),
    ]