# Generated by Django 3.0.7 on 2021-02-18 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0107_auto_20210217_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitydeclaration',
            name='reminder_count',
            field=models.IntegerField(default=0),
        ),
    ]
