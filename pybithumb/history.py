import requests
import datetime
import pandas as pd


def get_ohlcv(symbol="BTC", interval="day"):
    try:
        if interval == "minute":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_01M.json".format(symbol)
        elif interval == "minute3":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_03M.json".format(symbol)
        elif interval == "minute5":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_05M.json".format(symbol)
        elif interval == "minute10":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_10M.json".format(symbol)
        elif interval == "minute30":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_30M.json".format(symbol)
        elif interval == "hour":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_01H.json".format(symbol)
        elif interval == "hour6":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_06H.json".format(symbol)
        elif interval == "hour12":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_12H.json".format(symbol)
        else:
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_24H.json".format(symbol)

        r = requests.get(url)
        contents = r.json()

        ohlcv_list = []
        date_list = []
        for x in contents:
            timestamp = x[0]
            date = datetime.datetime.fromtimestamp(timestamp/1000)
            date_list.append(date)
            ohlcv = {'open': float(x[1]), 'high': float(x[3]), 'low': float(x[4]), 'close': float(x[2]), 'volume': float(x[5])}
            ohlcv_list.append(ohlcv)

        df = pd.DataFrame(ohlcv_list, columns=['open', 'high', 'low', 'close', 'volume'], index=date_list)
        return df
    except:
        return None


if __name__ == "__main__":
    df = get_ohlcv("BTC", interval="minute5")
    print(df.head())
