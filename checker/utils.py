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
        for tag in soup2.select("div.realperson-challenge"):
            tag.decompose()

        human_readed_html =  soup2.body.decode()

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
    
# https://nuvola.madisoft.it/bacheca-digitale/bacheca/TSPC02000N/1/IN_PUBBLICAZIONE/0/show
# https://www.carduccidante.edu.it/albo-online?cerca=&categoria=0&tipo=albo-online&aoo=
# https://www.voltatrieste.edu.it/albo-online
# https://www.deledda-fabiani.it/albo-online
# https://www.liceo-oberdan.edu.it/albo-online
# https://www.trasparenzascuole.it/Public/APDPublic_ExtV2.aspx?CF=80020660322
# https://www.trasparenzascuole.it/Public/APDPublic_ExtV2.aspx?CF=80019860321
# https://www.trasparenzascuole.it/Public/APDPublic_ExtV2.aspx?CF=80017410327
# https://drive.google.com/drive/folders/1ZuPSUC9MfYK_UFERp6QQzsrso7affHzq
# https://isitgo.it/albo/
# https://web.spaggiari.eu/sdg2/AlboOnline/GOII0001
# https://web.spaggiari.eu/sdg2/AlboOnline/goii0007?page=1
# https://web.spaggiari.eu/sdg2/AlboOnline/GOII0004
# https://web.spaggiari.eu/sdg2/AlboOnline/goii0009
# https://www.linussio.edu.it/albo-online
# https://web.spaggiari.eu/sdg2/Interpelli/UDII0001
# https://web.spaggiari.eu/sdg2/AlboOnline/UDII0009
# https://www.cnpd.it/albo-online
# https://web.spaggiari.eu/sdg2/AlboOnline/UDEF0002
# https://www.isisfermosolari.edu.it/albo-online?categoria=10001&cerca=&storico=&aoo=
# https://www.tarvisioscuole.it/pagine/graduatorie
# https://www.tarvisioscuole.it/archivio-news
# https://www.liceopercoto.edu.it/albo-online?categoria=10001&cerca=&storico=&aoo=
# https://www.arteudine.edu.it/albo-online
# https://web.spaggiari.eu/sdg2/AlboOnline/udlg0001?idCategoria=10004
# https://www.isismanzini.edu.it/pagine/interpelli
# https://www.liceogrigoletti.edu.it/albo-online
# https://www.liceoartisticogalvani.edu.it/archivio-news
# https://web.spaggiari.eu/sdg2/Interpelli/PNLS0004
# https://www.leomajor.edu.it/albo-online
# https://www.torricellimaniago.edu.it/servizi?id=507&&source=servizi-personale
# https://www.liceipujati.edu.it/albo-online
# https://web.spaggiari.eu/sdg2/AlboOnline/UDII0013?page=1
# https://www.isismagrinimarchetti.edu.it/novita/le-notizie/
# https://www.isismagrinimarchetti.edu.it/documento/la-segreteria-comunica-2/
# https://www.isismagrinimarchetti.edu.it/servizio/la-segreteria-comunica/
# https://www.isislatisana.edu.it/albo-online
# https://web.spaggiari.eu/sdg2/AlboOnline/UDLS0002?page=1
# https://web.spaggiari.eu/sdg2/AlboOnline/UDLS0001