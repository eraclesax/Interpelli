# app/management/commands/check_pages.py
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from checker.models import MonitoredPage
from checker.utils import check_page

class Command(BaseCommand):
    """
    Come usarlo? Lancia: 
        python manage.py check_pages
    (Fai ciò che devi fare sui link cambiati)
    Resetta le info con:
        python manage.py import_links links.txt --reset
    Reimposta gli hash con:
        python manage.py check_pages
    """
    help = "Controlla se le pagine monitorate sono cambiate"

    def handle(self, *args, **kwargs):
        logger = logging.getLogger("app")
        logger.info(f"\nNuovo check: {timezone.now()}")
        counter = 0
        total = MonitoredPage.objects.count()
        for page in MonitoredPage.objects.all():
            changed = check_page(page)
            if changed:
                self.stdout.write(self.style.SUCCESS(f"{counter}/{total} La pagina è cambiata: {page.url}"))
                logger.info(f"Cambiata: {page.url} (ultimo check: {page.last_checked})")
            else:
                self.stdout.write(f"{counter}/{total} Nessun cambiamento: {page.url}")

