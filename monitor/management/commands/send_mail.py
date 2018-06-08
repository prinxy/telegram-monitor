from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

from datetime import datetime
from monitor.models import PinnedMessage, Recipient


class Command(BaseCommand):
    help = 'Checks for any new pinned messages and sends an email.'

    def handle(self, *args, **options):
        unsent_messages = PinnedMessage.objects.filter(
            sent=False).select_related('channel')
        if unsent_messages.exists():
            mail = ''
            count = 1
            for msg in unsent_messages:
                mail += '{}. FROM CHANNEL: {}\n Pinned Message: {}\n\n'.format(
                    count,
                    msg.channel.name,
                    msg.text
                )
                count += 1
            recipients = [
                r.email for r in Recipient.objects.filter(active=True)
            ]
            try:
                send_mail(
                    'New Pinned Messages: {}'.format(datetime.now()),
                    mail,
                    'pydevtester@gmail.com',
                    recipients,
                    fail_silently=False
                )
                unsent_messages.update(sent=True)
            except Exception as e:
                print('Error')
                print(e)
