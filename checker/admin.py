from django.contrib import admin
from .models import *

class MonitoredPageAdmin(admin.ModelAdmin):
    pass

admin.site.register(MonitoredPage, MonitoredPageAdmin)
