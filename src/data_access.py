import csv
from models import Titolo, Portafoglio


# ---------------------------------------------------------
#  CARICA COSTI DI GESTIONE (acquisto + vendita)
# ---------------------------------------------------------
def carica_costi_gestione(path="data/costi_gestione.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        row = next(reader)

        return {
            "spese_acquisto": float(row["spese_acquisto"]),
            "commissioni_acquisto": float(row["commissioni_acquisto"]),
            "spese_vendita": float(row["spese_vendita"]),
            "commissioni_vendita": float(row["commissioni_vendita"])
        }


# ---------------------------------------------------------
#  CARICA PORTAFOGLIO (CSV PULITO)
# ---------------------------------------------------------
def carica_portafoglio_da_csv(percorso_file):
    portafoglio = Portafoglio()

    with open(percorso_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            titolo = Titolo(
                isin=row["isin"],
                symbol=row["symbol"],
                nome=row["nome"],
                quantita=row["quantita"],
                prezzo_carico=row["prezzo_carico"],
                data_acquisto=row["data_acquisto"]
            )

            portafoglio.aggiungi_titolo(titolo)

    return portafoglio