# Generated by Django 3.2 on 2021-04-29 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0133_auto_20210428_1450'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
            migrations.RemoveField(
                model_name='dbscertificatescope',
                name='certificate',
            ),
            migrations.RemoveField(
                model_name='dbscertificatescope',
                name='scope',
            ),
            migrations.RemoveField(
                model_name='entitydbstradingcertificate',
                name='certificate',
            ),
            migrations.RemoveField(
                model_name='entitydbstradingcertificate',
                name='entity',
            ),
            migrations.RemoveField(
                model_name='entityiscctradingcertificate',
                name='certificate',
            ),
            migrations.RemoveField(
                model_name='entityiscctradingcertificate',
                name='entity',
            ),
            migrations.RemoveField(
                model_name='entityredcerttradingcertificate',
                name='certificate',
            ),
            migrations.RemoveField(
                model_name='entityredcerttradingcertificate',
                name='entity',
            ),
            migrations.RemoveField(
                model_name='iscccertificaterawmaterial',
                name='certificate',
            ),
            migrations.RemoveField(
                model_name='iscccertificatescope',
                name='certificate',
            ),
            migrations.RemoveField(
                model_name='iscccertificatescope',
                name='scope',
            ),
            migrations.RemoveField(
                model_name='productionsitecertificate',
                name='certificate_2bs',
            ),
            migrations.RemoveField(
                model_name='productionsitecertificate',
                name='certificate_iscc',
            ),
            migrations.RemoveField(
                model_name='productionsitecertificate',
                name='certificate_redcert',
            ),
            migrations.RemoveField(
                model_name='productionsitecertificate',
                name='certificate_sn',
            ),
            migrations.RemoveField(
                model_name='productionsitecertificate',
                name='entity',
            ),
            migrations.RemoveField(
                model_name='productionsitecertificate',
                name='production_site',
            ),
            migrations.RemoveField(
                model_name='redcertcertificate',
                name='country',
            ),
            migrations.RemoveField(
                model_name='redcertcertificatebiomass',
                name='biomass',
            ),
            migrations.RemoveField(
                model_name='redcertcertificatebiomass',
                name='certificate',
            ),
            migrations.RemoveField(
                model_name='redcertcertificatescope',
                name='certificate',
            ),
            migrations.RemoveField(
                model_name='redcertcertificatescope',
                name='scope',
            ),
            migrations.DeleteModel(
                name='DBSCertificate',
            ),
            migrations.DeleteModel(
                name='DBSCertificateScope',
            ),
            migrations.DeleteModel(
                name='DBSScope',
            ),
            migrations.DeleteModel(
                name='EntityDBSTradingCertificate',
            ),
            migrations.DeleteModel(
                name='EntityISCCTradingCertificate',
            ),
            migrations.DeleteModel(
                name='EntityREDCertTradingCertificate',
            ),
            migrations.DeleteModel(
                name='ISCCCertificate',
            ),
            migrations.DeleteModel(
                name='ISCCCertificateRawMaterial',
            ),
            migrations.DeleteModel(
                name='ISCCCertificateScope',
            ),
            migrations.DeleteModel(
                name='ISCCScope',
            ),
            migrations.DeleteModel(
                name='ProductionSiteCertificate',
            ),
            migrations.DeleteModel(
                name='REDCertBiomassType',
            ),
            migrations.DeleteModel(
                name='REDCertCertificate',
            ),
            migrations.DeleteModel(
                name='REDCertCertificateBiomass',
            ),
            migrations.DeleteModel(
                name='REDCertCertificateScope',
            ),
            migrations.DeleteModel(
                name='REDCertScope',
            ),],
            database_operations=[],
        )
    ]