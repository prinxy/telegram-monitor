from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

from datetime import datetime
from monitor.models import PinnedMessages


class Command(BaseCommand):
    help = 'Checks for any new pinned messages.'

    def handle(self, *args, **options):
        pass
