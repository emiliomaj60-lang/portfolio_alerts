from flask import Blueprint, render_template
from data_access import carica_portafoglio_da_csv

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/")
def index():
    portafoglio = carica_portafoglio_da_csv("data/portfolio.csv")
    titoli = portafoglio.lista_titoli()
    return render_template("index.html", titoli=titoli)