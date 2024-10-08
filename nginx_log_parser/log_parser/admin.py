from django.contrib import admin
from log_parser.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp', 'http_method', 'url', 'response_code')
    search_fields = ('ip_address', 'url')
    list_filter = ('http_method', 'response_code')
