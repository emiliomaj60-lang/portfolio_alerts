import requests
import os
import yfinance as yf

API_KEY = os.getenv("RAPIDAPI_KEY")

print("DEBUG → API_KEY:", API_KEY)

# ---------------------------------------------------------
# 1️⃣ FUNZIONE ORIGINALE: RapidAPI
# ---------------------------------------------------------
def get_price_rapidapi(symbol):
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
        print("DEBUG → ERROR RapidAPI:", e)
        return None


# ---------------------------------------------------------
# 2️⃣ NUOVA FUNZIONE: yfinance (fallback)
# ---------------------------------------------------------
def get_price_yf(symbol):
    try:
        print("DEBUG → yfinance request:", symbol)

        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")

        if data.empty:
            print("DEBUG → yfinance: no data")
            return None

        prezzo = float(data["Close"].iloc[-1])
        print("DEBUG → yfinance price:", prezzo)
        return prezzo

    except Exception as e:
        print("DEBUG → ERROR yfinance:", e)
        return None


# ---------------------------------------------------------
# 3️⃣ FUNZIONE UNIFICATA: prova RapidAPI → fallback yfinance
# ---------------------------------------------------------
def get_price(symbol):
    # 1. Prova RapidAPI
    prezzo = get_price_rapidapi(symbol)
    if prezzo is not None:
        return prezzo

    print("DEBUG → RapidAPI fallita, uso yfinance")

    # 2. Fallback yfinance
    return get_price_yf(symbol)