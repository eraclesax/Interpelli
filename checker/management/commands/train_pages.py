# app/management/commands/train_pages.py
from django.core.management.base import BaseCommand
from time import sleep
from checker.models import MonitoredPage
from checker.utils import fetch_clean_html

class Command(BaseCommand):
    help = "Addestra il sistema a riconoscere falsi positivi salvando i numeri di riga instabili"

    def add_arguments(self, parser):
        parser.add_argument("--delay", type=int, default=5,
                            help="Secondi di attesa tra i due controlli consecutivi")

    def handle(self, *args, **options):
        delay = options["delay"]
        
        for page in MonitoredPage.objects.all():
            html1 = fetch_clean_html(page.url)
            sleep(delay)  # piccolo delay per sicurezza
            html2 = fetch_clean_html(page.url)

            lines1 = html1.splitlines()
            lines2 = html2.splitlines()

            # trova differenze di riga
            ignored = []
            for i, (l1, l2) in enumerate(zip(lines1, lines2)):
                if l1 != l2:
                    ignored.append(i)

            # salva in DB
            page.ignored_lines = ignored
            page.last_html = html2
            page.save()

            self.stdout.write(self.style.SUCCESS(
                f"{page.url}: {len(ignored)} righe instabili ignorate"
            ))