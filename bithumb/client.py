import base64
import hashlib
import hmac
import time
import urllib
import requests


class client:
    def __init__(self, conkey, seckey):
        self.API_CONKEY = conkey.encode('utf-8')
        self.API_SECRET = seckey.encode('utf-8')

        self.session = requests.session()
        self.session.headers.update({'Api-Key': self.API_CONKEY})

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
        return self._post('/info/balance', **kwargs)

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
        return self._get(uri, **kwargs)

    def _get(self, uri, **kwargs):
        URL = "https://api.bithumb.com" + uri
        return self.session.get(url=URL, params=kwargs).json()

    def _post(self, uri, **kwargs):
        kwargs.update({'endpoint': uri})
        target = [uri, urllib.parse.urlencode(kwargs), str(int(time.time() * 1000))]

        # generate signature
        query_string = chr(0).join(target).encode('utf-8')
        h = hmac.new(self.API_SECRET, query_string, hashlib.sha512)
        api_sign = base64.b64encode(h.hexdigest().encode('utf-8'))

        # send
        URL = "https://api.bithumb.com" + uri
        self.session.headers['Api-Sign'] = api_sign
        self.session.headers['Api-Nonce'] = target[2]
        return self.session.post(url=URL, data=kwargs).json()


if __name__ == "__main__":
    bithumb = client('CONKEY', 'SECKEY')

    # 잔고 조회
    response = bithumb.get_balance(currency="ETH")
    print(response)

    # 최근 거래 완료 내역
    response = bithumb.get_transactions(count=4)
    for p in response['data']:
        print ("최근 체결가:", p['price'])

    response = bithumb.get_transactions()
    print("최근 체결가", response['data'][0]['price'])

    response = bithumb.get_transactions(coin="ETH")
    print("최근 체결가", response['data'][0]['price'])
