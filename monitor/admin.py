from django.contrib import admin

from .models import Configuration, PinnedMessage, TargetChannel

admin.site.register(Configuration)
admin.site.register(PinnedMessage)
admin.site.register(TargetChannel)
