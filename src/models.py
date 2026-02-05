from datetime import datetime

class Titolo:
    def __init__(self, isin, symbol, nome, quantita, prezzo_carico,
                 spese_commissioni, spese_fisse, data_acquisto):
        
        self.isin = isin
        self.symbol = symbol
        self.nome = nome
        self.quantita = float(quantita)
        self.prezzo_carico = float(prezzo_carico)
        self.spese_commissioni = float(spese_commissioni)
        self.spese_fisse = float(spese_fisse)

        # data in formato italiano gg/mm/aaaa
        self.data_acquisto = datetime.strptime(data_acquisto, "%d/%m/%Y")

    def valore_totale_carico(self):
        """Valore totale investito su questo titolo (inclusi costi)."""
        return (self.prezzo_carico * self.quantita) + self.spese_commissioni + self.spese_fisse

    def __str__(self):
        return (f"{self.nome} ({self.symbol}) - ISIN: {self.isin}\n"
                f" Quantità: {self.quantita}\n"
                f" Prezzo carico: {self.prezzo_carico} €\n"
                f" Spese: comm={self.spese_commissioni} €, fisse={self.spese_fisse} €\n"
                f" Data acquisto: {self.data_acquisto.strftime('%d/%m/%Y')}\n")
        

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