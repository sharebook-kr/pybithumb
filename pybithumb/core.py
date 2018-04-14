import base64
import hashlib
import hmac
import time
import urllib
import requests


class RestApi:
    def __init__(self, conkey, seckey):
        self.http = BithumbHttp(conkey, seckey)

    def balance(self, **kwargs):
        """
        pybithumb 거래소 회원 지갑 정보
        :param currency: 코인 타입        
        :return: json type
        {
            "status"    : "0000",
            "data"      : {
                "total_btc"     : "665.40127447",
                "total_krw"     : "305507280",
                "in_use_btc"    : "127.43629364",
                "in_use_krw"    : "8839047.0000000000",
                "available_btc" : "537.96498083",
                "available_krw" : "294932685.000000000000",
                "xcoin_last"    : "505000"
            }
        }        
        """
        return self.http.post('/info/balance', **kwargs)

    def recent_transactions(self, **kwargs):
        """
        거래소 거래 체결 완료 내역
        :param coin: Coin 이름
        :param count: 조회할 데이터의 개수
        :return: json type
        {
            "status"    : 결과 상태 코드
            "data"      : [
                {
                    "transaction_date"  : 거래 채결 시간
                    "type"              : 판/구매 (ask, bid)
                    "units_traded"      : 거래 Currency 수량
                    "price"             : 1Currency 거래 금액
                    "total"             : 총 거래금액
                }...               
            ]
        }
        """
        coin = kwargs.get('coin', None)
        if coin is None:
            coin = "BTC"
        else:
            del (kwargs['coin'])

        uri = "/public/recent_transactions/" + coin
        print(kwargs)
        return self.http.get(uri, **kwargs)

    def place(self, **kwargs):
        """    
        매수/매도 주문을 발행한다
        :param type: 구매/판매 구분자로 "bid", "ask" 중 하나의 값을 갖는다
        :param currency: Bithumb의 코인 타입 
        :param unit: 수량
        :param price: 단가         
        :return: json type
        {
            "status"    : "0000",
            "order_id"  : "1428646963419",
            "data": [
                {
                    "cont_id"   : "15313",
                    "units"     : "0.61460000",
                    "price"     : "284000",
                    "total"     : 174546,
                    "fee"       : "0.00061460"
                },
                {
                    "cont_id"   : "15314",
                    "units"     : "0.18540000",
                    "price"     : "289000",
                    "total"     : 53581,
                    "fee"       : "0.00018540"
                }
            ]
        }
        """
        return self.http.post('/trade/place', **kwargs)

    def orders(self, **kwargs):
        return self.http.post('/info/orders', **kwargs)

    def cancel(self, **kwargs):
        return self.http.post('/trade/cancel', **kwargs)


class HttpMethod:
    def __init__(self):
        self.session = requests.session()

    @property
    def base_url(self):
        return ""

    def _handle_response(self, response):
        """        
        requests에 대한 error handling
        """
        # statue code가 000이 아닐경우, requests.exceptions.HTTPError 발생
        # 이부분은 에러처리를 어떻게 할 것인지 논의를 더 해 봐야 함
        # response.raise_for_status()
        return response.json()

    def update_headers(self, headers):
        self.session.headers.update(headers)

    def post(self, path, timeout=1, **kwargs):
        uri = self.base_url + path
        response = self.session.post(url=uri, data=kwargs, timeout=timeout)
        return self._handle_response(response)

    def get(self, path, timeout=1, **kwargs):
        uri = self.base_url + path
        response = self.session.get(url=uri, params=kwargs, timeout=timeout)
        return self._handle_response(response)


class BithumbHttp(HttpMethod):
    def __init__(self, conkey, seckey):
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
