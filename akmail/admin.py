from django.contrib import admin
from .models import Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'from_email', 'receiver_email', 'folder', 'is_starred', 'sent_at')
    list_filter = ('folder', 'is_starred', 'sent_at')
    search_fields = ('subject', 'from_email', 'receiver_email', 'message')
    ordering = ('-sent_at',)

admin.site.register(Email, EmailAdmin)