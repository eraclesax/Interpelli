# app/models.py
from django.db import models

class MonitoredPage(models.Model):
    url = models.URLField(unique=True)
    last_content_hash = models.CharField(max_length=64, blank=True, null=True)
    last_checked = models.DateTimeField(blank=True, null=True)
    has_changed = models.BooleanField(default=False)

    def __str__(self):
        return self.url
