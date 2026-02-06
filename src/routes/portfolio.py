from flask import Blueprint, render_template, jsonify

# Import corretti per Railway (che esegue dentro /app/src)
from data_access import carica_portafoglio_da_csv, carica_costi_gestione
from market_api import get_price

import os

print("FILE PRESENTI IN SRC:", os.listdir("/app/src"))
print("DEBUG → import data_access:", carica_portafoglio_da_csv)
print("DEBUG → import market_api:", get_price)

portfolio_bp = Blueprint("portfolio", __name__)


# ---------------------------------------------------------
#  PAGINA PRINCIPALE DEL PORTAFOGLIO
# ---------------------------------------------------------
@portfolio_bp.route("/")
def index():
    # Carica il portafoglio dal CSV
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")

    # Ottieni la lista dei titoli (oggetti)
    titoli = portafoglio.lista_titoli()

    for t in titoli:
        symbol = t.symbol

        # Per titoli italiani, aggiungiamo .MI se manca
        if "." not in symbol:
            symbol = symbol + ".MI"

        # Chiamata API
        prezzo = get_price(symbol)
        print("DEBUG → chiamata API:", symbol, prezzo)

        # Salva il prezzo attuale nell’oggetto
        t.prezzo_attuale = prezzo

        # Calcolo gain/loss percentuale
        if prezzo:
            t.gain_loss = ((prezzo - t.prezzo_carico) / t.prezzo_carico) * 100
        else:
            t.gain_loss = None

    # Passiamo i titoli al template
    return render_template("index.html", portafoglio=titoli)


# ---------------------------------------------------------
#  ENDPOINT: aggiorna un singolo titolo
# ---------------------------------------------------------
@portfolio_bp.route("/refresh/<symbol>")
def refresh_price(symbol):
    # Aggiungi .MI se manca
    original_symbol = symbol
    if "." not in symbol:
        symbol = symbol + ".MI"

    prezzo = get_price(symbol)

    print("DEBUG → refresh:", symbol, prezzo)

    return jsonify({
        "symbol": original_symbol,
        "prezzo": prezzo
    })


# ---------------------------------------------------------
#  PAGINA SCHEDA RIASSUNTIVA
# ---------------------------------------------------------
@portfolio_bp.route("/scheda/<symbol>")
def scheda(symbol):
    # Carica portafoglio
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")
    titoli = portafoglio.lista_titoli()

    # Trova il titolo richiesto
    titolo = next((t for t in titoli if t.symbol == symbol), None)

    if not titolo:
        return "Titolo non trovato", 404

    # Carica costi gestione
    costi = carica_costi_gestione()

    # --- CALCOLI DI ACQUISTO ---
    valore_acquisto = titolo.prezzo_carico * titolo.quantita
    spese_fisse_acq = costi["spese_acquisto"]
    commissioni_acq = valore_acquisto * (costi["commissioni_acquisto"] / 100)
    totale_speso = valore_acquisto + spese_fisse_acq + commissioni_acq

    # --- CALCOLI DI VENDITA ---
    prezzo_attuale = titolo.prezzo_attuale
    valore_vendita = prezzo_attuale * titolo.quantita

    spese_fisse_vend = costi["spese_vendita"]
    commissioni_vend = valore_vendita * (costi["commissioni_vendita"] / 100)

    totale_incassato = valore_vendita - spese_fisse_vend - commissioni_vend

    # --- GUADAGNO NETTO ---
    guadagno_netto = totale_incassato - totale_speso

    return render_template(
        "scheda.html",
        titolo=titolo,
        costi=costi,
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