import requests

def get_price(symbol):
    """
    Recupera il prezzo attuale del titolo usando Yahoo Finance.
    Ritorna None se il prezzo non è disponibile.
    """

    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        result = data["quoteResponse"]["result"]
        if not result:
            return None

        return result[0].get("regularMarketPrice", None)

    except Exception:
        return None