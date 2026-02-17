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

        # Storico lotti
        self.lotti = [{
            "quantita": self.quantita,
            "prezzo": self.prezzo_carico,
            "data": self.data_acquisto
        }]

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
        self.titoli = {}   # dict con chiave ISIN

    def aggiungi_titolo(self, titolo):
        isin = titolo.isin

        # Se è il primo lotto → aggiungilo
        if isin not in self.titoli:
            self.titoli[isin] = titolo
            return

        # Se esiste già → AGGREGA
        esistente = self.titoli[isin]

        q = float(titolo.quantita)
        p = float(titolo.prezzo_carico)

        # Aggiorna quantità totale
        esistente.quantita += q

        # Aggiorna valore totale
        esistente.valore_totale += q * p

        # Prezzo medio ponderato
        esistente.prezzo_carico = esistente.valore_totale / esistente.quantita

        # Mantieni la data più vecchia
        if titolo.data_acquisto < esistente.data_acquisto:
            esistente.data_acquisto = titolo.data_acquisto

        # Aggiungi lotto allo storico
        esistente.lotti.append({
            "quantita": q,
            "prezzo": p,
            "data": titolo.data_acquisto
        })

    def get_titolo(self, isin):
        return self.titoli.get(isin)

    def lista_titoli(self):
        return list(self.titoli.values())