from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from monitor.models import PinnedMessage, Configuration, TargetChannel
from monitor.monitor import get_pinned_message


class Command(BaseCommand):
    help = 'Extracts pinned messages from all channels and saves any new ones.'

    def handle(self, *args, **options):
        config = Configuration.objects.get()
        target_channels = TargetChannel.objects.all()

        for channel in target_channels:
            pinned_message = get_pinned_message(
                config.username,
                config.api_id,
                config.api_hash,
                channel.name
            )
            if pinned_message:
                msg = pinned_message.messages[0]
                channel.channel_id = msg.to_id.channel_id
                channel.save()
                pm_id = msg.id
                text = msg.message
                already_exists = PinnedMessage.objects.filter(
                    channel=channel).filter(message_id=pm_id).exists()
                if not already_exists:
                    pinned_obj = PinnedMessage(
                        channel=channel,
                        message_id=pm_id,
                        text=text
                    )
                    pinned_obj.save()

        # pinned_messages = PinnedMessage.objects.all()
        # return pinned_messages
