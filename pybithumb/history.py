import requests
import datetime
import pandas as pd

def get_ohlcv(symbol="BTC", interval="day"):
    try:
        if interval == "hour":
            url = "https://www.bithumb.com/resources/chart/{}_xcoinTrade_01H.json".format(symbol)
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
            ohlcv = {'open': x[1], 'high': x[3], 'low': x[4], 'close': x[2], 'volume': x[5]}
            ohlcv_list.append(ohlcv)

        df = pd.DataFrame(ohlcv_list, columns=['open', 'high', 'low', 'close', 'volume'], index=date_list)
        return df
    except:
        return None


if __name__ == "__main__":
    #print(get_ohlcv("BTC"))
    print(get_ohlcv("BTC", interval="hour"))
