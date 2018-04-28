from pybithumb.core import *


class Bithumb:
    def __init__(self, conkey, seckey):
        self.api = privateApi(conkey, seckey)

    @staticmethod
    def get_tickers():
        return ["BTC", "ETH", "DASH", "LTC", "ETC", "XRP", "BCH", "XMR", "ZEC", "QTUM",
                "BTG", "EOS", "ICX", "VEN", "TRX", "ELF", "MITH", "MCO", "OMG", "KNC"]

    @staticmethod
    def get_market_detail(currency):
        """
        거래소 마지막 거래 정보
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :return        : (24시간저가, 24시간고가, 24시간평균거래금액, 24시간거래량)
        """
        resp = publicApi.ticker(currency)
        low    = resp['min_price']
        high   = resp['max_price']
        avg    = resp['average_price']
        volume = resp['units_traded']
        return float(low), float(high), float(avg), float(volume)

    @staticmethod
    def get_current_price(currency):
        """
        최종 체결 가격을 얻어오는 메서드
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :return        : price
        """
        return publicApi.recent_transactions(currency)[0]['price']

    @staticmethod
    def get_orderbook(currency):
        """
        매수/매도 호가를 얻어오는 메서드
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :return        : 매수/매도 호가
        """
        return publicApi.orderbook(currency)

    def get_balance(self, currency):
        """
        거래소 회원의 잔고를 얻어오는 메서드
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :return        : (보유코인, 사용중코인, 보유원화, 사용중원화)
        """
        resp = self.api.balance(currency=currency)
        specifier = currency.lower()
        return (float(resp["total_" + specifier]), float(resp["in_use_" + specifier]),
                float(resp["total_krw"]), float(resp["in_use_krw"]))

    def put_order(self, type, currency, payment, price, unit):
        r = self.api.place(type=type, price=price, units=unit, order_currency=currency,
                           Payment_currency=payment)
        return (type, currency, r['order_id'])

    def get_order(self, order_desc):
        return self.api.orders(type=order_desc[0], currency=order_desc[1], order_id=order_desc[1])

    def put_cancel(self, order_desc):
        return self.api.cancel(type=order_desc[0], currency=order_desc[1], order_id=order_desc[1])


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------
    # 최종 체결 가격
    # ----------------------------------------------------------------------------------------------
    # for coin in Bithumb.get_tickers():
    #     print(coin, Bithumb.get_current_price(coin))

    # ----------------------------------------------------------------------------------------------
    # 시장 현황 상세정보
    # ----------------------------------------------------------------------------------------------
    # for coin in  Bithumb.get_tickers():
    #     print(coin, Bithumb.get_market_detail(coin))

    # ----------------------------------------------------------------------------------------------
    # 매수/매도 호가
    # ----------------------------------------------------------------------------------------------
    # for coin in  Bithumb.get_tickers():
    #     print(coin, Bithumb.get_orderbook(coin))

    import csv
    keys = next(csv.reader(open("keys.csv")))
    bithumb = Bithumb(keys[0].strip(), keys[1].strip())

    # ----------------------------------------------------------------------------------------------
    # 잔고 조회
    # ----------------------------------------------------------------------------------------------
    # for coin in Bithumb.get_tickers():
    #     print(coin, bithumb.get_balance(coin))


    # info = c.put_order("ask", "XRP", 1000, 1000)
    # print (info)
    # r = c.get_order(info)
    # print (r)
    # r = c.put_cancel(info)
    # print(response)









