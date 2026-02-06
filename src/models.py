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

    def valore_totale_carico(self):
        """Valore totale investito (solo prezzo × quantità)."""
        return self.prezzo_carico * self.quantita

    def __str__(self):
        return (
            f"{self.nome} ({self.symbol}) - ISIN: {self.isin}\n"
            f" Quantità: {self.quantita}\n"
            f" Prezzo carico: {self.prezzo_carico} €\n"
            f" Data acquisto: {self.data_acquisto.strftime('%d/%m/%Y')}\n"
        )


class Portafoglio:
    def __init__(self):
        self.titoli = {}

    def aggiungi_titolo(self, titolo):
        """Aggiunge un titolo al portafoglio usando ISIN come chiave."""
        self.titoli[titolo.isin] = titolo

    def get_titolo(self, isin):
        return self.titoli.get(isin)

    def lista_titoli(self):
        return list(self.titoli.values())

    def stampa_riepilogo(self):
        print("\n=== RIEPILOGO PORTAFOGLIO ===\n")
        for titolo in self.lista_titoli():
            print(titolo)
            print("-" * 40)