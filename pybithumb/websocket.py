import websockets
import asyncio
import json
import multiprocessing as mp


class WebSocketManager(mp.Process):
    """웹소켓을 관리하는 클래스

        사용 예제:

            >> wm = WebSocketManager("ticker", ["BTC_KRW"])
            >> for i in range(3):
                data = wm.get()
                print(data)
            >> wm.terminate()

        주의 :

           재귀적인 호출을 위해 다음의 guard를 반드시 추가해야 한다.
           >> if __name__ == "__main__"

    """
    def __init__(self, type: str, symbols: list, ticktype: list=None, qsize: int=1000):
        """웹소켓을 컨트롤하는 클래스의 생성자

        Args:
            type     (str           ): 구독 메시지 종류 (ticker/transaction/orderbookdepth)
            symbols  (list          ): 구독할 암호 화폐의 리스트 [BTC_KRW, ETH_KRW, …]
            ticktype (list, optional): tick 종류 리스트 (30M/1H/12H/24H/MID)
            qsize    (int , optional): 메시지를 저장할 Queue의 크기
        """
        self.__q = mp.Queue(qsize)
        self.alive = False

        self.type = type
        self.symbols = symbols

        self.ticktype = ticktype
        if self.ticktype == None:
            self.ticktype = ["1H"]
        super().__init__()

    async def __connect_socket(self):
        uri = "wss://pubwss.bithumb.com/pub/ws"

        async with websockets.connect(uri, ping_interval=None) as websocket:
            connection_msg = await websocket.recv()
            # {"status":"0000","resmsg":"Connected Successfully"}
            if "Connected Successfully" not in connection_msg :
                print("connection error")

            data = {
                "type"     : self.type,
                'symbols'  : self.symbols,
                'tickTypes': self.ticktype
            }
            await websocket.send(json.dumps(data))

            registration_msg = await websocket.recv()
            # {"status":"0000","resmsg":"Filter Registered Successfully"}
            if "Filter Registered Successfully" not in registration_msg:
                print("Registration error")

            while self.alive:
                recv_data = await websocket.recv()
                self.__q.put(json.loads(recv_data))

    def run(self):
        self.__aloop = asyncio.get_event_loop()
        self.__aloop.run_until_complete(self.__connect_socket())

    def get(self):
        if self.alive == False:
            self.alive = True
            self.start()
        return self.__q.get()

    def terminate(self):
        self.alive = False
        super().terminate()
