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
        거래소 마지막 거래 정보 조회
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
        최종 체결 가격 조회
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :return        : price
        """
        return publicApi.recent_transactions(currency)[0]['price']

    @staticmethod
    def get_orderbook(currency):
        """
        매수/매도 호가 조회
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :return        : 매수/매도 호가
        """
        return publicApi.orderbook(currency)

    def get_balance(self, currency):
        """
        거래소 회원의 잔고 조회
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :return        : (보유코인, 사용중코인, 보유원화, 사용중원화)
        """
        resp = self.api.balance(currency=currency)
        specifier = currency.lower()
        return (float(resp["total_" + specifier]), float(resp["in_use_" + specifier]),
                float(resp["total_krw"]), float(resp["in_use_krw"]))

    def buy_limit_order(self, currency, price, unit):
        """
        매수 주문
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :param price   : 주문 가격
        :param unit    : 주문 수량
        :return        : (주문Type, currency, 주문ID)
        """
        nit = "{0:.4f}".format(unit)
        order_id = self.api.place(type="bids", price=price, units=unit, order_currency=currency)
        return "bids", currency, order_id

    def sell_limit_order(self, currency, price, unit):
        """
        매도 주문
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :param price   : 주문 가격
        :param unit    : 주문 수량
        :return        : (주문Type, currency, 주문ID)
        """
        unit = "{0:.4f}".format(unit)
        order_id = self.api.place(type="asks", price=price, units=unit, order_currency=currency)
        return "asks", currency, order_id

    def get_outstanding_order(self, order_desc):
        """
        거래 미체결 수량 조회
        :param order_desc: (주문Type, currency, 주문ID)
        :return          : 거래 미체결 수량
        """
        resp =  self.api.orders(type=order_desc[0], currency=order_desc[1], order_id=order_desc[2])
        # HACK : 빗썸이 데이터를 리스트에 넣어줌
        return resp[0]['units_remaining']

    def cancel_order(self, order_desc):
        """
        매수/매도 주문 취소
        :param order_desc: (주문Type, currency, 주문ID)
        :return          : 성공: 0000 / 실패: message
        """
        return self.api.cancel(type=order_desc[0], currency=order_desc[1], order_id=order_desc[2])

    def buy_market_order(self, currency, unit):
        """
        시장가 매수
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :param unit    : 주문수량
        :return        : (판매단가, 판매수량)
        """
        resp = self.api.market_buy(currency=currency, units=unit)
        return resp['price'], resp['units']

    def sell_market_order(self, currency, unit):
        """
        시장가 매도
        :param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN,TRX/ELF/MITH/MCO/OMG/KNC
        :param unit    : 주문수량
        :return        : (판매단가, 판매수량)
        """
        resp = self.api.market_sell(currency=currency, units=unit)
        return resp['price'], resp['units']


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

    # ----------------------------------------------------------------------------------------------
    # 매도 주문
    # ----------------------------------------------------------------------------------------------
    # desc = bithumb.sell_limit_order("BTC", 11000000, 0.00844498)
    # print(desc)
    # desc = bithumb.buy_limit_order("BTC", 11000000, 0.00844498)
    # print(desc)

    # ----------------------------------------------------------------------------------------------
    # 매수/매도 잔량 확인
    # ----------------------------------------------------------------------------------------------
    # quanity = bithumb.get_outstanding_order(desc)
    # print(quanity)

    # ----------------------------------------------------------------------------------------------
    # 매수/매도 주문 취소
    # ----------------------------------------------------------------------------------------------
    # resp = bithumb.cancel_order(desc)
    # print(resp)

