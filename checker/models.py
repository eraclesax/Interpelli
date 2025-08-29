# app/models.py
from django.db import models

class MonitoredPage(models.Model):
    url = models.URLField(unique=True)
    last_html = models.TextField(blank=True, null=True)
    last_checked = models.DateTimeField(blank=True, null=True)
    has_changed = models.BooleanField(default=False)

    # lista dei numeri di riga da ignorare
    ignored_lines = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.url
    
    def get_ignored_lines(self):
        if not self.ignored_lines:
            return []
        return self.ignored_lines.split("\n")
    
    def add_ignored_lines(self, lines):
        existing = set(self.get_ignored_lines())
        existing.update(lines)
        self.ignored_lines = "\n".join(sorted(existing))
