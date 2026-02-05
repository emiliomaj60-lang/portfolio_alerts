from flask import Blueprint, render_template

# Import dai moduli nella stessa cartella "src"
from data_access import carica_portafoglio_da_csv
from market_api import get_price

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/")
def index():
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")
    titoli = portafoglio.lista_titoli()

    for t in titoli:
        symbol = t.symbol

        # Per titoli italiani, se non c'è un punto, aggiungo .MI
        if "." not in symbol:
            symbol = symbol + ".MI"

        t.prezzo_attuale = get_price(symbol)

        if t.prezzo_attuale:
            t.gain_loss = ((t.prezzo_attuale - t.prezzo_carico) / t.prezzo_carico) * 100
        else:
            t.gain_loss = None

    return render_template("index.html", titoli=titoli)