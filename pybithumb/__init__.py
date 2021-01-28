from pybithumb.client import Bithumb
from .history import *
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

def get_candlestick(order_currency, payment_currency="KRW", chart_instervals="24h"):
    return Bithumb.get_candlestick(order_currency, payment_currency, chart_instervals)