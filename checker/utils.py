# app/utils.py
import requests
import hashlib
from datetime import datetime
from django.utils import timezone
from .models import MonitoredPage

def check_page(page: MonitoredPage):
    try:
        response = requests.get(page.url, timeout=10)
        response.raise_for_status()
        html = response.text

        # calcola hash del contenuto
        new_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()

        if page.last_content_hash and new_hash != page.last_content_hash:
            page.has_changed = True
        else:
            page.has_changed = False

        page.last_content_hash = new_hash
        print(new_hash)
        page.last_checked = timezone.now()
        page.save()

        return page.has_changed

    except Exception as e:
        print(f"Errore con {page.url}: {e}")
        return False
