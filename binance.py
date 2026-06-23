import requests

def get_binance_buy_rate():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": "BUY",
        "page": 1,
        "rows": 1
    }

    data = requests.post(url, json=payload).json()
    price = data["data"][0]["adv"]["price"]
    return round(float(price), 4)

def get_binance_sell_rate():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": "SELL",
        "page": 1,
        "rows": 1
    }

    data = requests.post(url, json=payload).json()
    price = data["data"][0]["adv"]["price"]
    return round(float(price), 4)