from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from monitor.models import Recipient


class Command(BaseCommand):
    help = 'Mails each recipient a link to the summary page.'

    def handle(self, *args, **options):
        target_channels = TargetChannel.objects.all()
        recipients = [r.email for r in Recipient.objects.filter(active=True)
        message = 'Summary link for the last 24 Hours: https://ringindiadom.pythonanywhere.com/monitor/summary/ '

        send_mail(
            'Summary mail for {}'.format(datetime.now()),
            message,
            'ringtelegram@gmail.com',
            recipients,
            fail_silently=False
        )
