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

    prezzi_salvati = carica_prezzi_attuali()
    costi = carica_costi_gestione()

    totale_speso_portafoglio = 0
    totale_incassato_portafoglio = 0

    for t in titoli:

        # --- PREZZO ATTUALE ---
        t.prezzo_attuale = prezzi_salvati.get(t.symbol, None)

        # --- GAIN/LOSS ---
        if t.prezzo_attuale:
            try:
                t.gain_loss = ((t.prezzo_attuale - t.prezzo_carico) / t.prezzo_carico) * 100
            except:
                t.gain_loss = None
        else:
            t.gain_loss = None

        # --- CALCOLI ACQUISTO ---
        valore_acq = t.prezzo_carico * t.quantita

        comm_acq = valore_acq * (costi["commissioni_acquisto"] / 100)
        if comm_acq < costi["commis_min_acquisto"]:
            comm_acq = costi["commis_min_acquisto"]

        totale_speso = valore_acq + costi["spese_acquisto"] + comm_acq
        totale_speso_portafoglio += totale_speso

        # --- SE NON HO PREZZO ATTUALE ---
        if not t.prezzo_attuale:
            t.guadagno_netto = None
            continue

        # --- CALCOLI VENDITA ---
        valore_vend = t.prezzo_attuale * t.quantita

        comm_vend = valore_vend * (costi["commissioni_vendita"] / 100)
        if comm_vend < costi["commis_min_vendita"]:
            comm_vend = costi["commis_min_vendita"]

        totale_incassato = valore_vend - costi["spese_vendita"] - comm_vend
        totale_incassato_portafoglio += totale_incassato

        t.guadagno_netto = totale_incassato - totale_speso

    guadagno_totale = totale_incassato_portafoglio - totale_speso_portafoglio
    ultimo_agg = leggi_ultimo_aggiornamento()

    return render_template(
        "index.html",
        portafoglio=titoli,
        ultimo_aggiornamento=ultimo_agg,
        totale_speso_portafoglio=round(totale_speso_portafoglio, 2),
        totale_incassato_portafoglio=round(totale_incassato_portafoglio, 2),
        guadagno_totale=round(guadagno_totale, 2)
    )


# ---------------------------------------------------------
#  AGGIORNA UN SINGOLO TITOLO
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
#  AGGIORNA TUTTI I TITOLI
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

    salva_prezzi_attuali(prezzi)
    salva_ultimo_aggiornamento()

    return jsonify({"status": "ok"})


# ---------------------------------------------------------
#  PAGINA SCHEDA RIASSUNTIVA
# ---------------------------------------------------------
@portfolio_bp.route("/scheda/<chiave>")
def scheda(chiave):
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")

    titolo = portafoglio.get_titolo(chiave)
    if not titolo:
        return "Titolo non trovato", 404

    # Format data
    titolo.data_acquisto = titolo.data_acquisto.strftime("%d/%m/%Y")

    # Aggiorna prezzo
    api_symbol = titolo.symbol if "." in titolo.symbol else titolo.symbol + ".MI"
    titolo.prezzo_attuale = get_price(api_symbol)

    costi = carica_costi_gestione()

    # --- ACQUISTO ---
    prezzo_acquisto_unitario = titolo.prezzo_carico
    valore_acquisto = prezzo_acquisto_unitario * titolo.quantita
    spese_fisse_acq = costi["spese_acquisto"]

    commissioni_acq = valore_acquisto * (costi["commissioni_acquisto"] / 100)
    if commissioni_acq < costi["commis_min_acquisto"]:
        commissioni_acq = costi["commis_min_acquisto"]

    totale_speso = valore_acquisto + spese_fisse_acq + commissioni_acq

    # --- VENDITA ---
    prezzo_vendita_unitario = titolo.prezzo_attuale
    valore_vendita = prezzo_vendita_unitario * titolo.quantita
    spese_fisse_vend = costi["spese_vendita"]

    commissioni_vend = valore_vendita * (costi["commissioni_vendita"] / 100)
    if commissioni_vend < costi["commis_min_vendita"]:
        commissioni_vend = costi["commis_min_vendita"]

    totale_incassato = valore_vendita - spese_fisse_vend - commissioni_vend

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