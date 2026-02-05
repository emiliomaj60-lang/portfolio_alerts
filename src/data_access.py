import csv
from models import Titolo, Portafoglio

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
                spese_commissioni=row["spese_commissioni"],
                spese_fisse=row["spese_fisse"],
                data_acquisto=row["data_acquisto"]
            )
            portafoglio.aggiungi_titolo(titolo)

    return portafoglio
