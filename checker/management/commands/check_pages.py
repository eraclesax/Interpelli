# app/management/commands/check_pages.py
import logging
from django.utils import timezone
from django.core.management.base import BaseCommand
from checker.models import MonitoredPage
from checker.utils import fetch_clean_html, fetch_clean_html_from_url

class Command(BaseCommand):
    help = "Controlla le pagine monitorate escludendo le righe instabili"

    def handle(self, *args, **kwargs):
        logger = logging.getLogger("app")
        logger.info(f"\nNuovo check: {timezone.now()}")
        counter = 0
        total = MonitoredPage.objects.count()
            # === Leggi i link dal file ===
        for page in MonitoredPage.objects.all().order_by('pk'):
            counter += 1
            try:
                new_html = fetch_clean_html_from_url(page.url)
            except Exception as e:
                message = f"{counter}/{total} Error with url: {page.url}:\n{e}"
                self.stdout.write(self.style.ERROR(message))
                logger.info(message)
                continue
            if page.last_html:
                old_html = fetch_clean_html(page.last_html)
            else:
                old_html = ""

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
                self.stdout.write(self.style.WARNING(f"{counter}/{total} La pagina è cambiata: {page.url}"))
                logger.info(message)
            else:
                message = f"{counter}/{total} Nessun cambiamento: {page.url}"
                self.stdout.write(self.style.SUCCESS(message))
                logger.info(message)

            page.save()

