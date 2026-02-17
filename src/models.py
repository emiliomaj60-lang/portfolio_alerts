from datetime import datetime

class Titolo:
    def __init__(self, isin, symbol, nome, quantita, prezzo_carico, data_acquisto):
        
        self.isin = isin
        self.symbol = symbol
        self.nome = nome
        self.quantita = float(quantita)
        self.prezzo_carico = float(prezzo_carico)

        # data_acquisto nel CSV è in formato gg/mm/aaaa
        try:
            self.data_acquisto = datetime.strptime(data_acquisto, "%d/%m/%Y")
        except:
            # fallback se il CSV usa formato ISO (aaaa-mm-gg)
            self.data_acquisto = datetime.strptime(data_acquisto, "%Y-%m-%d")

        # Valori dinamici (riempiti in portfolio.py)
        self.prezzo_attuale = None
        self.gain_loss = None

        # Valore totale del lotto iniziale
        self.valore_totale = self.quantita * self.prezzo_carico

        # Storico lotti (per compatibilità)
        self.lotti = [{
            "quantita": self.quantita,
            "prezzo": self.prezzo_carico,
            "data": self.data_acquisto
        }]

        # La chiave unica verrà assegnata dal Portafoglio
        self.chiave = None


class Portafoglio:
    def __init__(self):
        self.titoli = {}   # dict con chiave UNICA per ogni lotto

    def aggiungi_titolo(self, titolo):
        # Creiamo una chiave unica per ogni lotto
        chiave = f"{titolo.isin}_{titolo.data_acquisto.strftime('%Y%m%d')}_{titolo.prezzo_carico}"

        # Salviamo la chiave dentro l'oggetto
        titolo.chiave = chiave

        # Ogni lotto è indipendente → nessuna aggregazione
        self.titoli[chiave] = titolo

    def get_titolo(self, chiave):
        return self.titoli.get(chiave)

    def lista_titoli(self):
        return list(self.titoli.values())