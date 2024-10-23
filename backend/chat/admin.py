from django.contrib import admin
from .models import ChatMessage


class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ["is_read"]
    list_display = ["sender", "receiver", "message", "is_read", "timestamp"]


admin.site.register(ChatMessage, ChatMessageAdmin)
