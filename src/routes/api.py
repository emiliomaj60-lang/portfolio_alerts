from flask import Blueprint, jsonify
from data_access import carica_portafoglio_da_csv

api_bp = Blueprint("api", __name__)

@api_bp.route("/portafoglio")
def api_portafoglio():
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")
    titoli = portafoglio.lista_titoli()

    data = []
    for t in titoli:
        data.append({
            "isin": t.isin,
            "symbol": t.symbol,
            "nome": t.nome,
            "quantita": t.quantita,
            "prezzo_carico": t.prezzo_carico
        })

    return jsonify(data)