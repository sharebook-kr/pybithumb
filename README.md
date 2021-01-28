# bithumb-api
Python Wrapper for Bithumb API

## Installation
```sh
pip install pybithumb
```

## Import
```python
from pybithumb import Bithumb
```

## Public API
####  암호화폐 목록
빗썸이 지원하는 암호화폐 목록을 얻어온다.
```python
print(Bithumb.get_tickers())
```
```
['BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP', 'BCH', 'XMR', 'ZEC', 'QTUM', 'BTG', 'EOS', 'ICX', 'TRX', 'ELF', 'MCO', 'OMG', 'KNC', 'GNT', 'ZIL', 'WAXP', 'POWR', 'LRC', 'STEEM', 'STRAT', 'AE', 'ZRX', 'REP', 'XEM', 'SNT', 'ADA', 'CTXC', 'BAT', 'WTC', 'THETA', 'LOOM', 'WAVES', 'ITC', 'TRUE', 'LINK', 'RNT', 'ENJ', 'PLX', 'VET', 'MTL', 'INS', 'IOST', 'TMTG', 'QKC', 'BZNT', 'HDAC', 'NPXS', 'LBA', 'WET', 'AMO', 'BSV', 'APIS', 'DAC', 'ORBS', 'VALOR', 'CON', 'ANKR', 'MIX', 'LAMB', 'CRO', 'FX', 'CHR', 'MBL', 'MXC', 'FAB', 'OGO', 'DVP', 'FCT', 'FNB', 'FZZ', 'TRV', 'PCM', 'DAD', 'AOA', 'XSR', 'WOM', 'SOC', 'EM', 'QBZ', 'BOA', 'WPX', 'FLETA', 'BNP', 'SXP', 'COS', 'EL', 'BASIC', 'HC', 'BCD', 'XVG', 'XLM', 'PIVX', 'GXC', 'BHP', 'BTT', 'HYC', 'VSYS', 'IPX', 'WICC', 'LUNA', 'AION', 'COSM']
```

#### 최근 체결가격
get_current_price 함수는 최근 체결 가격을 조회한다.
```python
for coin in Bithumb.get_tickers()[:5]:
    print(coin, Bithumb.get_current_price(coin))
```
```
BTC 8190000.0
ETH 171900.0
DASH 82450.0
LTC 48810.0
ETC 6180.0
```

#### 시장 현황 상세정보
get_market_detail 함수는 00시 기준으로 시가/고가/저가/종가/거래량 정보를 반환한다.
```python
for coin in  Bithumb.get_tickers():
    print(coin, Bithumb.get_market_detail(coin))
```
```
BTC (8162000.0, 8240000.0, 8050000.0, 8190000.0, 3117.77267769)
ETH (170500.0, 172600.0, 168000.0, 171500.0, 34816.2510681)
DASH (81950.0, 82700.0, 80600.0, 82450.0, 1651.47875125)
LTC (48440.0, 49410.0, 48270.0, 48810.0, 3344.70736905)
ETC (6150.0, 6250.0, 6075.0, 6180.0, 77986.83409064)
```
#### 매수/매도 호가
get_orderbook 함수는 호가 정보를 가져온다.
기본적으로 5개를 가져오며, limit 파라미터로 30개까지 지정할 수 있다.
```python
for coin in  Bithumb.get_tickers():
    print(coin, Bithumb.get_orderbook(coin))
```

#### 시간별 가격정보
시가/종가/고가/저가/거래량 정보를 DataFrame으로 반환한다.
```python
df = Bithumb.get_candlestick("BTC")
print(df.tail(5))
```

```python
                       open      close       high        low        volume
time
2020-03-30 15:00:00  7740000.0  7848000.0  8019000.0  7683000.0   7913.696718
2020-03-31 15:00:00  7847000.0  7630000.0  7893000.0  7534000.0   5163.670206
2020-04-01 15:00:00  7633000.0  8194000.0  8216000.0  7569000.0   9123.583777
2020-04-02 15:00:00  8193000.0  8162000.0  8499000.0  8057000.0  11354.950247
2020-04-04 08:00:00  8162000.0  8177000.0  8240000.0  8050000.0   3082.263414
```

chart_intervals 파라미터로 조회 간격을 조정할 수 있다.
- 1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h

```python
df = Bithumb.get_candlestick("BTC", chart_intervals="30m")
print(df.tail(5))
```

### 웹소켓
WebSocket을 이용해서 `현재가`, `호가`, `체결`에 대한 정보를 수신한다.
- 첫 번째 파라미터로 수신정보를 입력하며 `ticker`, `orderbook`, `transaction`을 사용할 수 있다.
- 두 번째 파라미터는 구독할 필터를 설정하며 암호화폐의 티커를 입력한다. 현재 버전에서는 원화 시장만을 지원한다.

```python
if __name__ == "__main__":
    wm = WebSocketManager("ticker", ["BTC_KRW"])
    for i in range(10):
        data = wm.get()
        print(data)
    wm.terminate()
```
주의할 사항은 multiprocessing을 위해 `__name__` guard를 반드시 써줘야한다는 것이다.

PyQt5와 함께 웹소켓을 사용하는 예제는 다음과 같다.
- 버튼을 클릭하면 웹소켓에서 가격정보를 가져와서 화면에 출력한다.
- https://gist.github.com/mr-yoo/a3d1f8a4152f94cf61e4bc566659cd20


## Private API
#### 로그인
connectkey와 secretkey를 사용해서 로그인한다.
두 key를 생성하는 방법은 [링크](http://sharebook.kr/x/ZQov)를 참조한다.
```python
bithumb = Bithumb("conkey", "seckey")
```

#### 수수료 조회
```python
print(bithumb.get_trading_fee())
```

#### 잔고 조회
```python
for coin in Bithumb.get_tickers():
    print(coin, bithumb.get_balance(coin))
```

#### 매수/매도 주문
비트코인을 1100만원에 1개 매수/매도한다.
```python
desc = bithumb.buy_limit_order("BTC", 11000000, 1)
desc = bithumb.sell_limit_order("BTC", 11000000, 1)
```

#### 매수/매도 잔량 확인
```python
quanity = bithumb.get_outstanding_order(desc)
```

#### 매수/매도 주문 취소
```python
status = bithumb.cancel_order(desc)
```

