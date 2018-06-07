from django.contrib import admin

from .models import Configuration, PinnedMessage, TargetChannel, Recipient

admin.site.register(Configuration)


@admin.register(PinnedMessage)
class PinnedMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'sent']


@admin.register(TargetChannel)
class TargetChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_id']


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['email', 'active']
