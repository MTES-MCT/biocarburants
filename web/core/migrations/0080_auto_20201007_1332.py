# Generated by Django 3.0.7 on 2020-10-07 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_iscccertificate_iscccertificaterawmaterial_iscccertificatescope_isccscope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iscccertificaterawmaterial',
            name='raw_material',
            field=models.CharField(max_length=128),
        ),
    ]