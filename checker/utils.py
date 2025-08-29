# app/utils.py
import requests
import difflib
import hashlib
from datetime import datetime
from django.utils import timezone
from bs4 import BeautifulSoup

from .models import MonitoredPage

def fetch_clean_html(url: str, selector: str = "body",exclude_selectors=["div.realperson-challenge", "span.footer-visite-count", "script"]) -> str:
    response = requests.get(url)
    response.raise_for_status()

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # rimuovi eventuali selettori esclusi
    if exclude_selectors:
        for sel in exclude_selectors:
            for tag in soup.select(sel):
                tag.decompose()

    target = soup.select_one(selector)
    relevant_html = target.decode() if target else html

    return relevant_html

# def check_page(page: MonitoredPage, selector: str = "body",exclude_selectors=["div.realperson-challenge", "span.footer-visite-count", "script"]):
#     """
#     Controlla se la pagina è cambiata rispetto all'ultimo check.
#     Di default confronta solo il tag <body>.
#     Puoi passare un CSS selector diverso, es: "div#content".
#     """
#     try:
#         response = requests.get(page.url, timeout=10)
#         response.raise_for_status()
#         html = response.text
#         soup = BeautifulSoup(html, "html.parser")

#         # rimuovi eventuali selettori esclusi
#         if exclude_selectors:
#             for sel in exclude_selectors:
#                 for tag in soup.select(sel):
#                     tag.decompose()

#         old_content = page.last_content or ""
#         new_lines = relevant_html.splitlines()
#         old_lines = old_content.splitlines()
        
#         # differenza riga per riga
#         diff = list(difflib.ndiff(old_lines, new_lines))
        
#         # estrai righe che appaiono cambiate
#         changed_lines = [line[2:] for line in diff if line.startswith("+ ") or line.startswith("- ")]
        
#         # escludi righe che sono già nella lista ignored
#         filtered_changes = [
#             line for line in changed_lines
#             if line not in page.get_ignored_lines()
#         ]

#         if filtered_changes:
#             page.has_changed = True
#         else:
#             page.has_changed = False

#         page.last_content = relevant_html
#         page.last_checked = timezone.now()
#         page.save()
        
#         return filtered_changes
        
#         # human_readed_html =  soup2.body.decode()
#         # # calcola hash del contenuto
#         # new_hash = hashlib.sha256(human_readed_html.encode("utf-8")).hexdigest()

#         # if page.last_content_hash and new_hash != page.last_content_hash:
#         #     page.has_changed = True
#         # else:
#         #     page.has_changed = False

#         # page.last_content_hash = new_hash
#         # page.last_checked = timezone.now()
#         # page.save()

#         # return page.has_changed
    

#     except Exception as e:
#         print(f"Errore con {page.url}: {e}")
#         return False