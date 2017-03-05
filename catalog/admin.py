from django.contrib import admin
from django.contrib.admin.models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'user', 'action_time')

admin.site.register(LogEntry, LogEntryAdmin)