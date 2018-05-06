import base64
import hashlib
import hmac
import time
import urllib
import requests


class publicApi:
    @staticmethod
    def ticker(currency):
        uri = "/public/ticker/" + currency
        return BithumbHttp().get(uri)

    @staticmethod
    def recent_transactions(currency):
        uri = "/public/recent_transactions/" + currency
        return BithumbHttp().get(uri)

    @staticmethod
    def orderbook(currency):
        uri = "/public/orderbook/" + currency
        return BithumbHttp().get(uri)


class privateApi:
    def __init__(self, conkey, seckey):
        self.http = BithumbHttp(conkey, seckey)

    def account(self, **kwargs):
        return self.http.post('/info/account', **kwargs)

    def balance(self, **kwargs):
        return self.http.post('/info/balance', **kwargs)

    def place(self, **kwargs):
        return self.http.post('/trade/place', **kwargs)

    def orders(self, **kwargs):
        return self.http.post('/info/orders', **kwargs)

    def cancel(self, **kwargs):
        return self.http.post('/trade/cancel', **kwargs)

    def market_buy(self, **kwargs):
        return self.http.post('/trade/market_buy', **kwargs)

    def market_sell(self, **kwargs):
        return self.http.post('/trade/market_sell', **kwargs)


class HttpMethod:
    def __init__(self):
        self.session = requests.session()

    @property
    def base_url(self):
        return ""

    def _handle_response(self, response):
        return response.json()

    def update_headers(self, headers):
        self.session.headers.update(headers)

    def post(self, path, timeout=3, **kwargs):
        uri = self.base_url + path
        response = self.session.post(url=uri, data=kwargs, timeout=timeout)
        return self._handle_response(response)

    def get(self, path, timeout=3, **kwargs):
        uri = self.base_url + path
        response = self.session.get(url=uri, params=kwargs, timeout=timeout)
        return self._handle_response(response)


class BithumbHttp(HttpMethod):
    def __init__(self, conkey="", seckey=""):
        self.API_CONKEY = conkey.encode('utf-8')
        self.API_SECRET = seckey.encode('utf-8')
        super(BithumbHttp, self).__init__()

    @property
    def base_url(self):
        return "https://api.bithumb.com"

    def _signature(self, path, nonce, **kwargs):
        query_string = path + chr(0) + urllib.parse.urlencode(kwargs) + chr(0) + nonce
        h = hmac.new(self.API_SECRET, query_string.encode('utf-8'), hashlib.sha512)
        return base64.b64encode(h.hexdigest().encode('utf-8'))

    def post(self, path, **kwargs):
        kwargs['endpoint'] = path
        nonce = str(int(time.time() * 1000))

        self.update_headers({
            'Api-Key': self.API_CONKEY,
            'Api-Sign': self._signature(path, nonce, **kwargs),
            'Api-Nonce': nonce
        })
        return super().post(path, **kwargs)

    def _handle_response(self, response):
        response = super()._handle_response(response)
        if response['status'] != '0000':
            return [response['message']]
        # [예외] buy/sell API의 결괏값은 'order_id'로 전송
        if response.get('order_id'):
            return response['order_id']
        # [예외] cancel API의 결괏값은 'status'만 전송
        if not response.get('data'):
            return response['status']
        # 빗썸 API 대부분의 정보는 'data'로 전송
        return response['data']