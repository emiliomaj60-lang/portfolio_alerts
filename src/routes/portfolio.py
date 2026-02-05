from flask import Blueprint, render_template

# Import corretti per Railway (che esegue dentro /app/src)
from data_access import carica_portafoglio_da_csv
from market_api import get_price

import os

print("FILE PRESENTI IN SRC:", os.listdir("/app/src"))
print("DEBUG → import data_access:", carica_portafoglio_da_csv)
print("DEBUG → import market_api:", get_price)

portfolio_bp = Blueprint("portfolio", __name__)

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

    # 🔥 QUI ERA IL PROBLEMA: ora passiamo la variabile giusta
    return render_template("index.html", portafoglio=titoli)