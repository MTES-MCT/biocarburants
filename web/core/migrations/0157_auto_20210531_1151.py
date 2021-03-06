# Generated by Django 3.2 on 2021-05-31 09:51

from django.db import migrations

def update_rights(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Rights = apps.get_model('core', 'UserRights')
    Requests = apps.get_model('core', 'UserRightsRequests')
    for right in Rights.objects.all():
        # update to RW
        if right.role == 'RO':
            right.role = 'RW'
            right.save()
        # create associated URR
        req, created = Requests.objects.get_or_create(user=right.user, entity=right.entity)
        if created:
            req.status = 'ACCEPTED'
        if req.role == 'RO':
            req.role = 'RW'
        req.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0156_alter_lottransaction_champ_libre'),
    ]

    operations = [
        migrations.RunPython(update_rights),
    ]

