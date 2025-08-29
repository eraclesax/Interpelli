from django.contrib import admin
from .models import *

class MonitoredPageAdmin(admin.ModelAdmin):
    list_display = ["pk", "last_checked","has_changed", "ignored_lines","url"]

admin.site.register(MonitoredPage, MonitoredPageAdmin)
