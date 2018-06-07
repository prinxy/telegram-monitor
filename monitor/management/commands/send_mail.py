from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

from datetime import datetime
from monitor.models import PinnedMessage, Recipient


class Command(BaseCommand):
    help = 'Checks for any new pinned messages and sends an email.'

    def handle(self, *args, **options):
        unsent_messages = PinnedMessage.objects.filter(
            sent=False).select_relate('channel')
        if unsent_messages.exist():
            mail = ''
            for msg in unsent_messages:
                mail += ' From Channel: {}\n Pinned Message: {}\n\n'.format(
                    msg.channel.name, msg.text)
            recipients = [
                r.email for r in Recipient.objects.filter(active=True)]
            try:
                send_mail(
                    'New Pinned Messages.',
                    mail,
                    'pydevtester@gmail.com',
                    recipients,
                    fail_silently=True
                )
                unsent_messages.update(sent=True)
            except:
                print('Error')
