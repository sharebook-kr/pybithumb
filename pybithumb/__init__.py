from pybithumb.client import Bithumb
from .history import *


def get_ohlc(currency):
    return Bithumb.get_ohlc(currency)


def get_tickers():
    return Bithumb.get_tickers()


def get_market_detail(currency):
    return Bithumb.get_market_detail(currency)


def get_current_price(currency):
    return Bithumb.get_current_price(currency)


def get_orderbook(currency, limit=5):
    return Bithumb.get_orderbook(currency, limit)
