# Generated by Django 3.0.7 on 2020-12-01 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0093_auto_20201125_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='biocarburant',
            name='is_displayed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='matierepremiere',
            name='is_displayed',
            field=models.BooleanField(default=True),
        ),
    ]
