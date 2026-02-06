import csv
import os
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


# ---------------------------------------------------------
#  SALVA PREZZI AGGIORNATI (SOLUZIONE A)
# ---------------------------------------------------------
def salva_prezzi_attuali(prezzi, path="data/prezzi_attuali.csv"):
    """
    prezzi = { "BFF": 4.35, "ENEL": 6.12, ... }
    """

    # Assicuriamoci che la cartella esista
    cartella = os.path.dirname(path)
    if cartella and not os.path.exists(cartella):
        os.makedirs(cartella)

    print("DEBUG → salvo prezzi:", prezzi)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "prezzo"])

        for symbol, prezzo in prezzi.items():
            if prezzo is not None:
                writer.writerow([symbol, prezzo])


# ---------------------------------------------------------
#  CARICA PREZZI AGGIORNATI (SOLUZIONE A)
# ---------------------------------------------------------
def carica_prezzi_attuali(path="data/prezzi_attuali.csv"):
    if not os.path.exists(path):
        return {}

    prezzi = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                prezzi[row["symbol"]] = float(row["prezzo"])
            except:
                pass

    return prezzi