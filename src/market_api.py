import requests
import os

API_KEY = os.getenv("RAPIDAPI_KEY")

print("DEBUG → API_KEY:", API_KEY)

def get_price(symbol):
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

        # Estrarre il prezzo dal percorso corretto
        chain = data.get("optionChain", {})
        result = chain.get("result", [])

        if result and "quote" in result[0]:
            quote = result[0]["quote"]
            if "regularMarketPrice" in quote:
                return float(quote["regularMarketPrice"])

        return None

    except Exception as e:
        print("DEBUG → ERROR:", e)
        return None