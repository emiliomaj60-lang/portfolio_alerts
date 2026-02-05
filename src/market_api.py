import requests
import os

API_KEY = os.getenv("RAPIDAPI_KEY")

print("DEBUG → API_KEY:", API_KEY)

def get_price(symbol):
    # Endpoint della tua API Yahoo Finance Real Time
    url = "https://yahoo-finance-real-time1.p.rapidapi.com/stock/get-options"

    params = {
        "symbol": symbol,
        "lang": "en-US",
        "region": "US"
    }

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()

        print("DEBUG → URL:", response.url)
        print("DEBUG → RESPONSE:", data)

        # Questa API NON restituisce direttamente il prezzo.
        # Dobbiamo estrarlo dal campo "underlying" → "regularMarketPrice"
        if "underlying" in data and "regularMarketPrice" in data["underlying"]:
            return float(data["underlying"]["regularMarketPrice"])

        return None

    except Exception as e:
        print("DEBUG → ERROR:", e)
        return None