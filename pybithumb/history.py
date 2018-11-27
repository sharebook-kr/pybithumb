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
        contents = requests.get(url).json()

        ohlcv = {}
        for x in contents:
            date = datetime.datetime.fromtimestamp(x[0]/1000)
            ohlcv[date] = [x[1], x[3], x[4], x[2], x[5]]
        df = pd.DataFrame.from_dict(ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], orient='index').astype(
                          dtype=float)
        return df
    except:
        return None


if __name__ == "__main__":
    df = get_ohlcv("BTC", interval="minute5")
    print(df)
    print(df.head())