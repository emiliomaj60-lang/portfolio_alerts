import requests
import os

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("DEBUG → API_KEY:", API_KEY)

def get_price(symbol):
    """
    Recupera il prezzo attuale usando Alpha Vantage.
    Supporta anche la Borsa Italiana (.MI).
    """

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
            return float(data["Global Quote"]["05. price"])

        return None

    except Exception as e:
        print("DEBUG → ERROR:", e)
        return None