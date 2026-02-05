import requests
import os
import time

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
print("DEBUG → API_KEY:", API_KEY)

CACHE = {}
CACHE_TTL = 60  # secondi

def get_price(symbol):
    now = time.time()

    # 1. Cache
    if symbol in CACHE:
        ts, price = CACHE[symbol]
        if now - ts < CACHE_TTL:
            print(f"DEBUG → CACHE HIT per {symbol}: {price}")
            return price

    # 2. API call con retry
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    )

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            print("DEBUG → URL:", url)
            print("DEBUG → RESPONSE:", data)

            # Risposta valida
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                price = float(data["Global Quote"]["05. price"])
                CACHE[symbol] = (now, price)
                return price

            # Rate limit → aspetta e riprova
            if "Information" in data or data == {}:
                print("DEBUG → RATE LIMIT, retry...")
                time.sleep(1)
                continue

            return None

        except Exception as e:
            print("DEBUG → ERROR:", e)
            return None

    return None