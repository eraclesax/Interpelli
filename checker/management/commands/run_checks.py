# app/management/commands/check_pages.py
import logging
from django.core.management.base import BaseCommand
from checker.models import MonitoredPage
from checker.utils import check_page

class Command(BaseCommand):
    help = "Controlla se le pagine monitorate sono cambiate"

    def handle(self, *args, **kwargs):
        for page in MonitoredPage.objects.all():
            changed = check_page(page)
            logger = logging.getLogger("app")
            if changed:
                self.stdout.write(self.style.SUCCESS(f"La pagina è cambiata: {page.url}"))
                logger.info(f"Cambiata: {page.url} alle {page.last_checked}")
            else:
                self.stdout.write(f"Nessun cambiamento: {page.url}")
