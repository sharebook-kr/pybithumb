from pybithumb.core import *
import datetime
import math


class Bithumb:
    def __init__(self, conkey, seckey):
        self.api = PrivateApi(conkey, seckey)

    @staticmethod
    def _convert_unit(unit):
        try:
            unit = math.floor(unit * 10000) / 10000
            return unit
        except:
            return 0

    @staticmethod
    def get_tickers(payment_currency="KRW"):
        """
        빗썸이 지원하는 암호화폐의 리스트
        :param payment_currency : KRW
        :return:
        """
        resp = None
        try:
            resp = PublicApi.ticker("ALL", payment_currency)
            data = resp['data']
            tickers = [k for k, v in data.items() if isinstance(v, dict)]
            return tickers
        except Exception:
            return resp

    @staticmethod
    def get_ohlc(order_currency, payment_currency="KRW"):
        """
        최근 24시간 내 암호 화폐의 OHLC의 튜플
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :return                 : 코인과 (시가, 고가, 저가, 종가) 가 딕셔너리로 저장
          {
            'BTC' : (7020000.0, 7093000.0, 6810000.0, 6971000.0)
            'ETH' : ( 720000.0,  703000.0,  681000.0,  697000.0)
          }
        """
        resp = None
        try:
            resp = PublicApi.ticker(order_currency, payment_currency)['data']
            if order_currency is "ALL":
                del resp['date']
                data = {}
                for key in resp:
                    data[key] = (
                        resp[key]['opening_price'], resp[key]['max_price'],
                        resp[key]['min_price'], resp[key]['closing_price'])
                return data

            return {
                order_currency: (
                    float(resp['opening_price']), float(resp['max_price']),
                    float(resp['min_price']),
                    float(resp['closing_price']))
            }
        except Exception:
            return resp

    @staticmethod
    def get_market_detail(order_currency, payment_currency="KRW"):
        """
        거래소 세부 정보 조회 (00시 기준)
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :return                 : (시가, 고가, 저가, 종가, 거래량)
        """
        resp = None
        try:
            resp = PublicApi.ticker(order_currency, payment_currency)
            open = resp['data']['opening_price']
            high = resp['data']['max_price']
            low = resp['data']['min_price']
            close = resp['data']['closing_price']
            volume = resp['data']['units_traded']
            return float(open), float(high), float(low), float(close), float(volume)
        except Exception:
            return resp

    @staticmethod
    def get_current_price(order_currency, payment_currency="KRW"):
        """
        최종 체결 가격 조회
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :return                 : price
        """
        resp = None
        try:
            resp = PublicApi.ticker(order_currency, payment_currency)
            if order_currency is not "ALL":
                return float(resp['data']['closing_price'])
            else:
                del resp["data"]['date']
                return resp["data"]
        except Exception:
            return resp

    @staticmethod
    def get_orderbook(order_currency, payment_currency="KRW", limit=5):
        """
        매수/매도 호가 조회
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :return                 : 매수/매도 호가
        """
        resp = None
        try:
            limit = min(limit, 20)
            resp = PublicApi.orderbook(order_currency, payment_currency, limit)
            data = resp['data']
            for idx in range(len(data['bids'])) :
                data['bids'][idx]['quantity'] = float(
                    data['bids'][idx]['quantity'])
                data['asks'][idx]['quantity'] = float(
                    data['asks'][idx]['quantity'])
                data['bids'][idx]['price'] = float(data['bids'][idx]['price'])
                data['asks'][idx]['price'] = float(data['asks'][idx]['price'])
            return data
        except Exception:
            return resp

    @staticmethod
    def get_btci():
        try:
            data = PublicApi.btci()['data']
            data['date'] = datetime.datetime.fromtimestamp(int(data['date']) / 1e3)
            return data
        except Exception:
            return None

    @staticmethod
    def get_candlestick(order_currency, payment_currency="KRW", chart_instervals="24h"):
        """
        Candlestick API
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :param chart_instervals : 24h {1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h 사용 가능}
        :return                 : (기준 시간, 시가, 고가, 저가, 종가, 거래량)
        """
        resp = None
        try:
            data = []
            resp = PublicApi.candlestick(order_currency=order_currency, payment_currency=payment_currency, chart_instervals=chart_instervals)
            if resp.get('status') == '0000':
                resp = resp.get('data')
                for idx in range(len(resp)):
                    time = int(resp[idx][0])
                    open = float(resp[idx][1])
                    close = float(resp[idx][2])
                    high = float(resp[idx][3])
                    low = float(resp[idx][4])
                    volume = float(resp[idx][5])
                    data.append(time, open, high, low, close, volume)
            return data
        except Exception:
            return resp

    def get_trading_fee(self, order_currency, payment_currency="KRW"):
        """
        거래 수수료 조회
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :return                 : 수수료
        """
        resp = None
        try:
            resp = self.api.account(order_currency=order_currency,
                                    payment_currency=payment_currency)
            return float(resp['data']['trade_fee'])
        except Exception:
            return resp

    def get_balance(self, currency):
        """
        거래소 회원의 잔고 조회
        :param currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :return           : (보유코인, 사용중코인, 보유원화, 사용중원화)
        """
        resp = None
        try:
            resp = self.api.balance(currency=currency)
            specifier = currency.lower()
            return (float(resp['data']["total_" + specifier]),
                    float(resp['data']["in_use_" + specifier]),
                    float(resp['data']["total_krw"]),
                    float(resp['data']["in_use_krw"]))
        except Exception:
            return resp

    def buy_limit_order(self, order_currency, price, unit,
                        payment_currency="KRW"):
        """
        매수 주문
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :param price            : 주문 가격
        :param unit             : 주문 수량
        :return                 : (주문Type, currency, 주문ID)
        """
        resp = None
        try:
            unit = Bithumb._convert_unit(unit)
            resp = self.api.place(type="bid", price=price, units=unit,
                                  order_currency=order_currency,
                                  payment_currency=payment_currency)
            return "bid", order_currency, resp['order_id'], payment_currency
        except Exception:
            return resp

    def sell_limit_order(self, order_currency, price, unit,
                         payment_currency="KRW"):
        """
        매도 주문
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :param price            : 주문 가격
        :param unit             : 주문 수량
        :return                 : (주문Type, currency, 주문ID)
        """
        resp = None
        try:
            unit = Bithumb._convert_unit(unit)
            resp = self.api.place(type="ask", price=price, units=unit,
                                  order_currency=order_currency,
                                  payment_currency=payment_currency)
            return "ask", order_currency, resp['order_id'], payment_currency
        except Exception:
            return resp

    def get_outstanding_order(self, order_desc):
        """
        거래 미체결 수량 조회
        :param order_desc: (주문Type, currency, 주문ID)
        :return          : 거래 미체결 수량
        """
        resp = None
        try:
            resp = self.api.orders(type=order_desc[0],
                                   order_currency=order_desc[1],
                                   order_id=order_desc[2],
                                   payment_currency=order_desc[3])
            if resp['status'] == '5600':
                return None
            # HACK : 빗썸이 데이터를 리스트에 넣어줌
            return resp['data'][0]['units_remaining']
        except Exception:
            return resp

    def get_order_completed(self, order_desc):
        """
        거래 완료 정보 조회
        :param order_desc: (주문Type, currency, 주문ID)
        :return          : 거래정보
        """
        resp = None
        try:
            resp = self.api.order_detail(type=order_desc[0],
                                         order_currency=order_desc[1],
                                         order_id=order_desc[2],
                                         payment_currency=order_desc[3])
            if resp['status'] == '5600':
                return None
            # HACK : 빗썸이 데이터를 리스트에 넣어줌
            return resp['data'][0]
        except Exception:
            return resp

    def cancel_order(self, order_desc):
        """
        매수/매도 주문 취소
        :param order_desc: (주문Type, currency, 주문ID)
        :return          : 성공: True / 실패: False
        """
        resp = None
        try:
            resp = self.api.cancel(type=order_desc[0],
                                   order_currency=order_desc[1],
                                   order_id=order_desc[2],
                                   payment_currency=order_desc[3])
            return resp['status'] == '0000'
        except Exception:
            return resp

    def buy_market_order(self, order_currency, unit, payment_currency="KRW"):
        """
        시장가 매수
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :param unit             : 주문수량
        :return                 : 성공 orderID / 실패 메시지
        """
        resp = None
        try:
            unit = Bithumb._convert_unit(unit)
            resp = self.api.market_buy(order_currency=order_currency,
                                       payment_currency=payment_currency,
                                       units=unit)
            return resp['order_id']
        except Exception:
            return resp

    def sell_market_order(self, order_currency, unit, payment_currency="KRW"):
        """
        시장가 매도
        :param order_currency   : BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        :param payment_currency : KRW
        :param unit             : 주문수량
        :return                 : 성공 orderID / 실패 메시지
        """
        resp = None
        try:
            unit = Bithumb._convert_unit(unit)
            resp = self.api.market_sell(order_currency=order_currency,
                                        payment_currency=payment_currency,
                                        units=unit)
            return resp['order_id']
        except Exception:
            return resp



if __name__ == "__main__":
    print(Bithumb.get_tickers())
    # print(Bithumb.get_orderbook("BTC"))
    # print(Bithumb.get_current_price("BTC"))
    # print(Bithumb.get_current_price("ALL"))