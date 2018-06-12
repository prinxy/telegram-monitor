from django.contrib import admin

from .models import Configuration, PinnedMessage, TargetChannel, Recipient


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'login_code', 'active']


@admin.register(PinnedMessage)
class PinnedMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'sent']
    search_fields = ['text']
    list_filters = ['sent', 'date_created']


@admin.register(TargetChannel)
class TargetChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_id']
    search_fields = ['name', 'channel_id']


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['email', 'active']
