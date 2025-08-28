# app/management/commands/import_links.py
from django.core.management.base import BaseCommand
from checker.models import MonitoredPage

class Command(BaseCommand):
    """
    Import semplice:
        python manage.py import_links links.txt
    Import con reset (ricalcola tutto):
        python manage.py import_links links.txt --reset
    Se un link sparisce da links.txt, viene rimosso dal DB.
    """
    help = "Importa link da un file di testo e sincronizza con il DB MonitoredPage"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Percorso del file con i link")
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Resetta gli hash e i flag delle pagine già presenti",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        reset = options["reset"]

        # === Leggi i link dal file ===
        try:
            with open(file_path, "r") as f:
                links = {
                    line.strip()
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                }
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File non trovato: {file_path}"))
            return

        # === Aggiungi/Aggiorna ===
        for link in links:
            page, created = MonitoredPage.objects.get_or_create(url=link)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Aggiunto: {link}"))
            else:
                if reset:
                    page.last_content_hash = None
                    page.has_changed = False
                    page.save()
                    self.stdout.write(
                        self.style.WARNING(f"Già presente (reset): {link}")
                    )
                else:
                    self.stdout.write(self.style.WARNING(f"Già presente: {link}"))

        # === Rimuovi i link non più nel file ===
        existing_links = set(MonitoredPage.objects.values_list("url", flat=True))
        to_delete = existing_links - links

        if to_delete:
            deleted_count, _ = MonitoredPage.objects.filter(url__in=to_delete).delete()
            for d in to_delete:
                self.stdout.write(self.style.ERROR(f"Rimosso: {d}"))
            self.stdout.write(self.style.ERROR(f"Totale rimossi: {deleted_count}"))
        else:
            self.stdout.write(self.style.SUCCESS("Nessun link da rimuovere"))
