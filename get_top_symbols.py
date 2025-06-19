from binance.client import Client

API_KEY = 'QCI76yYs5jbuYqS4geSkEZHhkPJq0QZCOz1pXGIEdIOvfN36Riiiiiiiiiiiiiii'
API_SECRET = 'EpMK5GTSHJxMFf42IhzGCpVLgxywR60Lz9lWDu7votvjLVgwiiiiiiiiiiiiiiii'

client = Client(API_KEY, API_SECRET)

def get_top_symbols(quote_asset="USDT", limit=100):
    tickers = client.get_ticker()  # Получаем последние цены всех символов
    volumes = {}

    for ticker in tickers:
        symbol = ticker['symbol']
        if symbol.endswith(quote_asset):
            try:
                depth = client.get_order_book(symbol=symbol, limit=5)
                bid_depth = float(depth['bids'][0][1]) if depth['bids'] else 0.0
                ask_depth = float(depth['asks'][0][1]) if depth['asks'] else 0.0
                volume = bid_depth + ask_depth
                volumes[symbol] = volume
            except Exception as e:
                print(f"⚠️ Ошибка при получении стакана {symbol}: {e}")

    # Сортируем по объему
    top_symbols = sorted(volumes.items(), key=lambda x: x[1], reverse=True)
    top_symbols = [s[0] for s in top_symbols[:limit]]
    
    return top_symbols

top_symbols = get_top_symbols()

print(f"Топ-{len(top_symbols)} активов:")
for s in top_symbols:
    print(s)
