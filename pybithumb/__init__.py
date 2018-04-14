from pybithumb.core import *
import pandas as pd


class Bithumb:
    def __init__(self, conkey, seckey):
        self.api = RestApi(conkey, seckey)

    def get_ticker(self, currency="BTC"):
        """
        bithumb 거래소 마지막 거래 정보
        :param currency:
        :return: dict
        """
        r = self.api.ticker(currency)
        return r.get('data')

    def get_transactions(self, count=10):
        r = self.api.recent_transactions(count=count)
        return pd.DataFrame(r['data'])

    def get_balance(self, currency):
        # out data format
        #{'total_krw': 0, 'in_use_krw': 0, 'available_krw': 0, 'misu_krw': 0, 'total_dash': '0.00000000',
        # 'in_use_dash': '0.00000000', 'available_dash': '0.00000000', 'misu_dash': 0, 'xcoin_last': '381000'}
        # df = pd.DataFrame()
        r = self.api.balance(currency=currency)
        # 어떻게 보여줄 것인지..
        return r['data']

    def put_order(self, type, currency, price, unit):
        r = self.api.place(type=type, price=price, units=unit, order_currency=currency)
        return (type, currency, r['order_id'])

    def get_order(self, order_desc):
        r = self.api.orders(type=order_desc[0], currency=order_desc[1], order_id=order_desc[1])
        return r

    def put_cancel(self, order_desc):
        r = self.api.cancel(type=order_desc[0], currency=order_desc[1], order_id=order_desc[1])
        return r


if __name__ == "__main__":
    bithumb = Bithumb('CONKEY', 'SECKEY')
    print(bithumb.get_transactions(20))
    print(bithumb.get_ticker("BTC"))

    # r = c.get_balance("DASH")
    # print (r)

    # info = c.put_order("ask", "XRP", 1000, 1000)
    # print (info)
    # r = c.get_order(info)
    # print (r)
    # r = c.put_cancel(info)
    # print(response)