from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages", null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True)  # Null for group chats
    message = models.TextField()
    deleted_by_user = models.BooleanField(default=False)  
    deleted_by_recipient = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
