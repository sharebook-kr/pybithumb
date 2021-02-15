from pybithumb.client import Bithumb
from .websocket import WebSocketManager

def get_ohlc(order_currency, payment_currency="KRW"):
    return Bithumb.get_ohlc(order_currency, payment_currency)


def get_tickers(payment_currency="KRW"):
    return Bithumb.get_tickers(payment_currency)


def get_market_detail(order_currency, payment_currency="KRW"):
    return Bithumb.get_market_detail(order_currency, payment_currency)


def get_current_price(order_currency, payment_currency="KRW"):
    return Bithumb.get_current_price(order_currency, payment_currency)


def get_orderbook(order_currency, payment_currency="KRW", limit=5):
    return Bithumb.get_orderbook(order_currency, payment_currency, limit)


def get_transaction_history(order_currency, payment_currency="KRW", limit=20):
    return Bithumb.get_transaction_history(order_currency, payment_currency, limit)

def get_candlestick(order_currency, payment_currency="KRW", chart_intervals="24h"):
    return Bithumb.get_candlestick(order_currency, payment_currency, chart_intervals)

# @util.deprecated('Please use get_candlestick() function instead of get_ohlcv().')
def get_ohlcv(order_currency="BTC", payment_currency="KRW", interval="day"):
    # for backward compatibility
    chart_instervals = {
        "day": "24h",
        "hour12": "12h",
        "hour6": "6h",
        "hour": "1h",
        "minute30": "30m",
        "minute10": "10m",
        "minute5": "5m",
        "minute3": "3m",
        "minute1": "1m",
    }[interval]

    return Bithumb.get_candlestick(order_currency, payment_currency, chart_instervals)