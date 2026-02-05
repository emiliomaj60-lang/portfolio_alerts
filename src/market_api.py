import requests
import os

API_KEY = os.getenv("TWELVEDATA_API_KEY")

print("DEBUG → API_KEY:", API_KEY)


def get_price(symbol):
    """
    Recupera il prezzo attuale usando TwelveData.
    Ritorna None se il prezzo non è disponibile.
    """

    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "price" in data:
            return float(data["price"])

        return None

    except Exception:
        return None