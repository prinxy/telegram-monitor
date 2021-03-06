from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import Configuration, PinnedMessage, TargetChannel
from .monitor import get_pinned_message


def index(request):
    config = Configuration.objects.get()
    target_channels = TargetChannel.objects.all()
    print(target_channels)

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

    pms = PinnedMessage.objects.all()
    context = {}
    for p in pms:
        context[p.channel.name] = p.text
    return JsonResponse(context)
