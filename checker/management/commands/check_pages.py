# app/management/commands/check_pages.py
import logging
from django.utils import timezone
from django.core.management.base import BaseCommand
from checker.models import MonitoredPage
from checker.utils import fetch_clean_html

class Command(BaseCommand):
    help = "Controlla le pagine monitorate escludendo le righe instabili"

    def handle(self, *args, **kwargs):
        logger = logging.getLogger("app")
        logger.info(f"\nNuovo check: {timezone.now()}")
        counter = 0
        total = MonitoredPage.objects.count()
        for page in MonitoredPage.objects.all():
            counter += 1
            new_html = fetch_clean_html(page.url)
            old_html = page.last_html or ""

            new_lines = new_html.splitlines()
            old_lines = old_html.splitlines()

            # escludi le righe instabili
            ignored = set(page.ignored_lines)

            diffs = []
            for i, (old, new) in enumerate(zip(old_lines, new_lines)):
                if i in ignored:
                    continue
                if old != new:
                    diffs.append((i, old, new))

            if len(new_lines) != len(old_lines):
                diffs.append(("lunghezza", len(old_lines), len(new_lines)))

            if diffs:
                page.has_changed = True
                page.last_html = new_html
                message = f"{counter}/{total} La pagina è cambiata: {page.url}\n" + \
                    "\n".join(f"  - Riga {i}: {o} -> {n}" for i, o, n in diffs if i != "lunghezza") +  \
                    ("\n  - Differenza di lunghezza" if any(i == "lunghezza" for i, _, _ in diffs) else "")
                self.stdout.write(self.style.WARNING(message))
                logger.info(message)
            else:
                message = f"{counter}/{total} Nessun cambiamento: {page.url}"
                self.stdout.write(self.style.SUCCESS(message))
                logger.info(message)

            page.save()


    # def handle(self, *args, **kwargs):
    #     logger = logging.getLogger("app")
    #     logger.info(f"\nNuovo check: {timezone.now()}")
    #     counter = 0
    #     total = MonitoredPage.objects.count()
    #     for page in MonitoredPage.objects.all():
    #         counter += 1
    #         changed = check_page(page)
    #         if changed:
    #             self.stdout.write(self.style.SUCCESS(f"{counter}/{total} La pagina è cambiata: {page.url}"))
    #             logger.info(f"Cambiata: {page.url} (ultimo check: {page.last_checked})")
    #         else:
    #             self.stdout.write(f"{counter}/{total} Nessun cambiamento: {page.url}")

