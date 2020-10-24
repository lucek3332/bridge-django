from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "to", "created")
    list_filter = ("author", "to", "created")
    search_fields = ("content", )


admin.site.register(Message, MessageAdmin)
