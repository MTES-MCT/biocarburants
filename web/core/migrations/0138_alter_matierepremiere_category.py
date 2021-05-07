# Generated by Django 3.2 on 2021-05-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0137_auto_20210430_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matierepremiere',
            name='category',
            field=models.CharField(choices=[('CONV', 'Conventionnel'), ('ANN-IX-A', 'ANNEXE IX-A'), ('ANN-IX-B', 'ANNEXE IX-B'), ('TALLOL', 'Tallol'), ('OTHER', 'Autre')], default='CONV', max_length=32),
        ),
    ]
