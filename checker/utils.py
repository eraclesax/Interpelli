# app/utils.py
import requests
import hashlib
from datetime import datetime
from django.utils import timezone
from bs4 import BeautifulSoup

from .models import MonitoredPage

def check_page(page: MonitoredPage, selector: str = "body"):
    """
    Controlla se la pagina è cambiata rispetto all'ultimo check.
    Di default confronta solo il tag <body>.
    Puoi passare un CSS selector diverso, es: "div#content".
    """
    try:
        response = requests.get(page.url, timeout=10)
        response.raise_for_status()
        html = response.text
        print(html)
        print("\n\n\n\n")
        soup1 = BeautifulSoup(html, "html.parser")

        # --- seleziona la parte rilevante ---
        target = soup1.select_one(selector)
        if not target:
            print(f"[WARN] Selettore {selector} non trovato per {page.url}, uso tutto l'HTML")
            relevant_html = html
        else:
            relevant_html = target.decode()  # ottieni solo l'HTML del blocco scelto

        soup2 = BeautifulSoup(relevant_html, "html.parser")
        # rimuovi div indesiderati
        EXCLUDE_SELECTORS = ["div.realperson-challenge", "span.footer-visite-count", "script"]
        for sel in EXCLUDE_SELECTORS:
            for tag in soup2.select(sel):
                tag.decompose()

        human_readed_html =  soup2.body.decode()
        print(human_readed_html)
        # calcola hash del contenuto
        new_hash = hashlib.sha256(human_readed_html.encode("utf-8")).hexdigest()

        if page.last_content_hash and new_hash != page.last_content_hash:
            page.has_changed = True
        else:
            page.has_changed = False

        page.last_content_hash = new_hash
        page.last_checked = timezone.now()
        page.save()

        return page.has_changed

    except Exception as e:
        print(f"Errore con {page.url}: {e}")
        return False