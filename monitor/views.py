import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from telethon import TelegramClient
from .models import Configuration, PinnedMessage, TargetChannel
from .forms import DateRangeForm, TelegramLoginCodeForm
from .monitor import get_pinned_message


@login_required(redirect_field_name='next', login_url='monitor:login')
def index(request, template='monitor/index.html'):
    # Before we display the index page, try and see if the Telegram client
    # Has Auth Access.
    config = Configuration.objects.filter(active=True).first()
    if not config:
        return Http404('No API credentials active')
    client = TelegramClient(
        config.username,
        config.api_id,
        config.api_hash,
        update_workers=0,
        spawn_read_thread=False
    )
    client.connect()
    if not client.is_authorized():
        client.send_code_request(config.phone)
        redirect('monitor:code')

    pinned_messages = PinnedMessage.objects.all().order_by('-date_created')
    context = {
        'pinned_messages': pinned_messages
    }
    return render(request, template, context)


@login_required(redirect_field_name='next', login_url='monitor:login')
def summary(request, template='monitor/summary.html'):
    channels = TargetChannel.objects.all()
    pinned_messages = PinnedMessage.objects.all().order_by('-date_created')
    new_pinned = [msg for msg in pinned_messages if msg.age() < 1]
    context = {
        'new_pinned_messages': new_pinned,
        'channels': channels
    }
    return render(request, template, context)


@login_required(redirect_field_name='next', login_url='monitor:login')
def search_dates(request, template='monitor/search_results.html'):
    form = DateRangeForm(request.GET or None)
    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        channel = form.cleaned_data['channel']
        # start = start - datetime.timedelta(days=1)
        end = end + datetime.timedelta(days=1)
        pinned_messages = PinnedMessage.objects.select_related(
            'channel'
        ).filter(date_created__range=(start, end)).order_by('channel')
        if channel:
            pinned_messages = pinned_messages.filter(
                channel__name__icontains=channel
            )
        context = {
            'form': form,
            'pinned_messages': pinned_messages
        }
        return render(request, template, context)

    return render(request, template, {'form': form})


@login_required(redirect_field_name='next', login_url='monitor:login')
def refresh(request):
    config = Configuration.objects.filter(active=True).first()
    target_channels = TargetChannel.objects.all()

    for channel in target_channels:
        pinned_message = get_pinned_message(
            config.username,
            config.api_id,
            config.api_hash,
            config.phone,
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
    return redirect('monitor:index')


def code(request, template='monitor/login.html'):
    config = Configuration.objects.filter(active=True).first()
    if not config:
        return Http404('No API credentials active')
    client = TelegramClient(
        config.username,
        config.api_id,
        config.api_hash,
        update_workers=0,
        spawn_read_thread=False
    )
    client.connect()
    form = TelegramLoginCodeForm(request.POST or None)
    code = request.POST.get('login_code', None)
    if code:
        try:
            client.sign_in(config.phone, code)
        except:
            form.add_error('login_code', 'Invalid Code')
    if form.is_valid():
        config.login_code = code
        config.save()
        redirect('monitor:summary')
    context = {
        'login_code_form': form
    }
    return render(request, context, template)
