from django.db import models

# Create your models here.


class Configuration(models.Model):
    api_id = models.IntegerField()
    api_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    username = models.CharField(max_length=255)

    def __str__(self):
        return '{}: {}'.format(self.username, self.phone)


class TargetChannel(models.Model):
    name = models.CharField(max_length=100)
    channel_id = models.CharField(max_length=255, null=True, blank=True)
    # member_count = models.IntegerField()

    def __str__(self):
        return '{}: {}'.format(self.name, self.channel_id)


class PinnedMessage(models.Model):
    channel = models.ForeignKey(
        TargetChannel,
        related_name='pinned_messages',
        on_delete=models.CASCADE
    )
    message_id = models.IntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    sent = models.BooleanField('Pinned message has been mailed', default=False)

    def __str__(self):
        return '{}: {}'.format(self.channel.name, self.text)


# class SentPinnedMessage(models.Model):
#     pinned_message = models.OneToOneField(
#         PinnedMessage,
#         on_delete=models.CASCADE
#     )
#     date_sent = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return '{}: {}'.format(self.pinned_message.channel, self.date_sent)


class Recipient(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.email)
