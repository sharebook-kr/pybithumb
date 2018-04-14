import base64
import hashlib
import hmac
import time
import urllib
import requests


class client:
    def __init__(self, conkey, seckey):
        self.http = BithumbHttp(conkey, seckey)

    def get_balance(self, **kwargs):
        """
        bithumb 거래소 회원 지갑 정보
        :param currency: 코인 타입
        :type currency: str
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

    def get_transactions(self, **kwargs):
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
        return self.http.get(uri, **kwargs)


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
        response = self.session.get(url=uri, data=kwargs, timeout=timeout)
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


if __name__ == "__main__":
    bithumb = client('', '')

    # 잔고 조회
    response = bithumb.get_balance(currency="ETH")
    print(response)

    # 최근 거래 완료 내역
    response = bithumb.get_transactions(count=4)
    for p in response['data']:
        print ("최근 체결가:", p['price'])
    #
    # response = bithumb.get_transactions()
    # print("최근 체결가:", response['data'][0]['price'])
    #
    # response = bithumb.get_transactions(coin="ETH")
    # print("최근 체결가:", response['data'][0]['price'])
