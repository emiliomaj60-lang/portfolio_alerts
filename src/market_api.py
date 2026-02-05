import requests
import os
import time

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("DEBUG → API_KEY:", API_KEY)

# Cache: simbolo → (timestamp, prezzo)
CACHE = {}
CACHE_TTL = 60  # secondi

def get_price(symbol):
    """
    Recupera il prezzo attuale usando Alpha Vantage.
    Usa una cache di 60 secondi per evitare rate limit.
    """

    now = time.time()

    # 1. Se il prezzo è in cache ed è recente → usalo
    if symbol in CACHE:
        ts, price = CACHE[symbol]
        if now - ts < CACHE_TTL:
            print(f"DEBUG → CACHE HIT per {symbol}: {price}")
            return price

    # 2. Altrimenti chiama l'API
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        print("DEBUG → URL:", url)
        print("DEBUG → RESPONSE:", data)

        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            price = float(data["Global Quote"]["05. price"])

            # Salva in cache
            CACHE[symbol] = (now, price)

            return price

        return None

    except Exception as e:
        print("DEBUG → ERROR:", e)
        return None