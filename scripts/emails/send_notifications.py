import os
import django
import datetime
from django.db.models import Count, Min, Max
from django.template import loader

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carbure.settings")
django.setup()


from core.models import EmailNotification, Entity

MAX_NOTIF_PER_HOUR = 10

def main():
    entities = Entity.objects.annotate(num_notifs=Count('emailnotification')).order_by('-num_notifs')

    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    email_notif_sent = 0

    entity_oldest_notif = {}

    for entity in entities:
        notifs = EmailNotification.objects.filter(entity=entity).aggregate(Count('id'), Min('datetime'), Max('datetime'))
        if notifs['id__count'] > 0:
            entity_oldest_notif[entity] = notifs['datetime__min']

    for entity, oldest_notif_dt in sorted(entity_oldest_notif.items(), key=lambda x: x[1]):
        # wait at least one hour before sending an email, in case more events are coming
        if oldest_notif_dt > one_hour_ago:
            print('Ignoring notifications for %s - Too soon' % (entity.name))
            continue

        notifs = EmailNotification.objects.filter(entity=entity)

        email_context = {
            'entity': entity,
            'notif_txs': [n for n in notifs if n.linked_tx != None],
            'notif_declarations': [n for n in notifs if n.linked_declaration != None]
        }
        html_message = loader.render_to_string('emails/notifications.html', email_context)
        text_message = loader.render_to_string('emails/notifications.txt', email_context)

#    email_subject = 'Carbure - Correction %s - %s - %.2f%%' % (tx.dae, tx.lot.biocarburant.name, tx.lot.ghg_reduction)##
#
#    if os.getenv('IMAGE_TAG', 'dev') != 'prod':
#        recipients = [r.user.email for r in UserRights.objects.filter(entity=tx.carbure_vendor, user__is_staff=True)]
#        cc = None
#


#    msg = EmailMultiAlternatives(subject=email_subject, body=text_message, from_email=settings.DEFAULT_FROM_EMAIL, to=recipients, cc=cc)
#    msg.attach_alternative(html_message, "text/html")
#    msg.send()
    
if __name__ == '__main__':
    main()
    
    