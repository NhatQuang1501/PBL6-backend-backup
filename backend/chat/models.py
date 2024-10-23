from django.db import models
from accounts.models import *
from application.models import *
from accounts.enums import *
import uuid


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )

    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
        verbose_name_plural = "Message"

    def __str__(self):
        return f"{self.sender} - {self.receiver} - {self.message}"

    @property
    def sender_profile(self):
        sender_profile = UserProfile.objects.get(user=self.sender)
        return sender_profile

    def receiver_profile(self):
        receiver_profile = UserProfile.objects.get(user=self.receiver)
        return receiver_profile
