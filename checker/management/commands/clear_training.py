# app/management/commands/clear_training.py
from django.core.management.base import BaseCommand
from checker.models import MonitoredPage
import logging

class Command(BaseCommand):
    help = "Resetta i numeri di riga ignorati (ignored_lines) per tutte le pagine"

    def handle(self, *args, **kwargs):
        logger = logging.getLogger("app")
        pages = MonitoredPage.objects.all()
        for page in pages:
            page.ignored_lines = []
            page.save()
        message = f"Reset effettuato per {pages.count()} pagine"
        self.stdout.write(self.style.SUCCESS(message))
        logger.info(message)