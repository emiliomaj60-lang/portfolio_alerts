import requests
import os

API_KEY = os.getenv("RAPIDAPI_KEY")

print("DEBUG → API_KEY:", API_KEY)

def get_price(symbol):
    url = f"https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{symbol}"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()

        print("DEBUG → URL:", url)
        print("DEBUG → RESPONSE:", data)

        # La risposta è una lista con un singolo elemento
        if isinstance(data, list) and len(data) > 0:
            return float(data[0]["regularMarketPrice"])

        return None

    except Exception as e:
        print("DEBUG → ERROR:", e)
        return None