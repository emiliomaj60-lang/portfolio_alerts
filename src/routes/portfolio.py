from flask import Blueprint, render_template, jsonify
from data_access import (
    carica_portafoglio_da_csv,
    carica_costi_gestione,
    carica_prezzi_attuali,
    salva_prezzi_attuali
)
from market_api import get_price
from datetime import datetime
import os

portfolio_bp = Blueprint("portfolio", __name__)


# ---------------------------------------------------------
#  GESTIONE FILE ULTIMO AGGIORNAMENTO
# ---------------------------------------------------------
def salva_ultimo_aggiornamento():
    with open("data/ultimo_aggiornamento.txt", "w") as f:
        f.write(datetime.now().strftime("%d/%m/%Y %H:%M"))

def leggi_ultimo_aggiornamento():
    try:
        with open("data/ultimo_aggiornamento.txt", "r") as f:
            return f.read().strip()
    except:
        return "Mai aggiornato"


# ---------------------------------------------------------
#  HOMEPAGE PORTAFOGLIO
# ---------------------------------------------------------
@portfolio_bp.route("/")
def index():
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")
    titoli = portafoglio.lista_titoli()

    # Carichiamo i prezzi salvati
    prezzi_salvati = carica_prezzi_attuali()

    # Applichiamo i prezzi e calcoliamo gain/loss
    for t in titoli:
        if t.symbol in prezzi_salvati:
            t.prezzo_attuale = prezzi_salvati[t.symbol]

            try:
                t.gain_loss = ((t.prezzo_attuale - t.prezzo_carico) / t.prezzo_carico) * 100
            except:
                t.gain_loss = None
        else:
            t.prezzo_attuale = None
            t.gain_loss = None

    ultimo_agg = leggi_ultimo_aggiornamento()

    return render_template("index.html", portafoglio=titoli, ultimo_aggiornamento=ultimo_agg)


# ---------------------------------------------------------
#  AGGIORNA UN SINGOLO TITOLO (scheda)
# ---------------------------------------------------------
@portfolio_bp.route("/refresh/<symbol>")
def refresh_price(symbol):
    original_symbol = symbol
    if "." not in symbol:
        symbol = symbol + ".MI"

    prezzo = get_price(symbol)

    return jsonify({
        "symbol": original_symbol,
        "prezzo": prezzo
    })


# ---------------------------------------------------------
#  AGGIORNA TUTTI I TITOLI (bottone homepage)
# ---------------------------------------------------------
@portfolio_bp.route("/aggiorna_tutti")
def aggiorna_tutti():
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")
    titoli = portafoglio.lista_titoli()

    prezzi = {}

    for t in titoli:
        api_symbol = t.symbol if "." in t.symbol else t.symbol + ".MI"
        prezzo = get_price(api_symbol)

        print("DEBUG →", t.symbol, "=", prezzo)

        if prezzo is not None:
            prezzi[t.symbol] = prezzo

    # Salviamo i prezzi aggiornati
    salva_prezzi_attuali(prezzi)

    # Salviamo l’ora dell’aggiornamento
    salva_ultimo_aggiornamento()

    return jsonify({"status": "ok"})


# ---------------------------------------------------------
#  PAGINA SCHEDA RIASSUNTIVA
# ---------------------------------------------------------
@portfolio_bp.route("/scheda/<symbol>")
def scheda(symbol):
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")
    titoli = portafoglio.lista_titoli()

    titolo = next((t for t in titoli if t.symbol == symbol), None)

    if not titolo:
        return "Titolo non trovato", 404

    # 🔵 FORMATTAZIONE DATA ACQUISTO IN STILE ITALIANO
    data_raw = str(titolo.data_acquisto).strip()

    try:
        # Caso: "2024-05-12 00:00:00"
        dt = datetime.strptime(data_raw, "%Y-%m-%d %H:%M:%S")
        titolo.data_acquisto = dt.strftime("%d/%m/%Y")
    except:
        try:
            # Caso: "2024-05-12"
            dt = datetime.strptime(data_raw, "%Y-%m-%d")
            titolo.data_acquisto = dt.strftime("%d/%m/%Y")
        except:
            # Se arriva già formattata o in altro formato, la lasciamo così
            pass

    # Aggiorniamo il prezzo solo per la scheda
    api_symbol = symbol if "." in symbol else symbol + ".MI"
    prezzo_attuale = get_price(api_symbol)
    titolo.prezzo_attuale = prezzo_attuale

    costi = carica_costi_gestione()

    # --- ACQUISTO ---
    prezzo_acquisto_unitario = titolo.prezzo_carico
    valore_acquisto = prezzo_acquisto_unitario * titolo.quantita
    spese_fisse_acq = costi["spese_acquisto"]

    # Calcolo percentuale
    commissioni_acq = valore_acquisto * (costi["commissioni_acquisto"] / 100)

    # Applica minimo
    if commissioni_acq < costi["commis_min_acquisto"]:
        commissioni_acq = costi["commis_min_acquisto"]

    totale_speso = valore_acquisto + spese_fisse_acq + commissioni_acq

    # --- VENDITA ---
    prezzo_vendita_unitario = prezzo_attuale
    valore_vendita = prezzo_vendita_unitario * titolo.quantita
    spese_fisse_vend = costi["spese_vendita"]

    # Calcolo percentuale
    commissioni_vend = valore_vendita * (costi["commissioni_vendita"] / 100)

    # Applica minimo
    if commissioni_vend < costi["commis_min_vendita"]:
        commissioni_vend = costi["commis_min_vendita"]

    totale_incassato = valore_vendita - spese_fisse_vend - commissioni_vend

    # --- GUADAGNO NETTO ---
    guadagno_netto = totale_incassato - totale_speso

    return render_template(
        "scheda.html",
        titolo=titolo,
        costi=costi,
        prezzo_acquisto_unitario=prezzo_acquisto_unitario,
        prezzo_vendita_unitario=prezzo_vendita_unitario,
        valore_acquisto=valore_acquisto,
        spese_fisse_acq=spese_fisse_acq,
        commissioni_acq=commissioni_acq,
        totale_speso=totale_speso,
        valore_vendita=valore_vendita,
        spese_fisse_vend=spese_fisse_vend,
        commissioni_vend=commissioni_vend,
        totale_incassato=totale_incassato,
        guadagno_netto=guadagno_netto
    )