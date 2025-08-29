# app/utils.py
import requests
import difflib
import hashlib
from datetime import datetime
from django.utils import timezone
from bs4 import BeautifulSoup

from .models import MonitoredPage

def fetch_clean_html_from_url(url: str, *args, **kwargs) -> str:
    response = requests.get(url)
    response.raise_for_status()

    cleaned_html = fetch_clean_html(response.text, *args, **kwargs)
    return cleaned_html

def fetch_clean_html(html: str, selector: str = "body",exclude_selectors=["div.realperson-challenge", "span.footer-visite-count", "script", "style"]) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # rimuovi eventuali selettori esclusi
    if exclude_selectors:
        for sel in exclude_selectors:
            for tag in soup.select(sel):
                tag.decompose()

    target = soup.select_one(selector)
    cleaned_html = target.decode() if target else html

    return cleaned_html
