import json
import datetime
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup


def get_ohlcv(order_currency="BTC", payment_currency="KRW", interval="day"):
    try:
        # for backward compatibility
        int2type = {
            "day": "24H",
            "hour12": "12H",
            "hour6": "06H",
            "hour": "01H",
            "minute30": "30M",
            "minute10": "10M",
            "minute5": "05M",
            "minute3": "03M",
        }

        url = "https://m.bithumb.com/trade/chart/{}_{}".format(order_currency,
                                                               payment_currency)
        resp = requests.get(url)
        html = resp.text

        # parsing coin type
        string = html.split("COIN = ")[1].split(";")[0]
        coin = json.loads(string)
        tk2ct = {v['symbol_name']: k for k, v in coin['C0100'].items()}

        # parsing xcoin name
        selector = "#barcodeForm > input[name=csrf_xcoin_name]"
        soup = BeautifulSoup(html, 'html5lib')
        xcoin_name = soup.select(selector)[0]['value']

        url = "https://m.bithumb.com/trade_history/chart_data"
        headers = {
            "cookie": 'csrf_xcoin_name={}'.format(xcoin_name),
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "coinType": tk2ct[order_currency],
            "crncCd": "C0100",
            "tickType": int2type[interval],
            "csrf_xcoin_name": xcoin_name
        }

        resp = requests.post(url, data=data, headers=headers).json()
        for x in resp['data']:
            x[0] = datetime.datetime.fromtimestamp(x[0] / 1000)

        columns = [order_currency, 'open', 'close', 'high', 'low', 'volume']
        df = DataFrame(resp['data'], columns=columns)
        df = df.set_index(order_currency)
        return df.astype(float)

    except:
        return None


if __name__ == "__main__":
    import time
    import pandas as pd
    pd.set_option('display.expand_frame_repr', False)
    for ticker in ["BTC", "LTC"]:
        df = get_ohlcv(ticker, interval="day")
        print(df.tail(2))
        time.sleep(0.3)
