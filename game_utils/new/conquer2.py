from requests import post, get
# from ..conquer2_game import conquer2_game
import asyncio
import json
import websockets


# conquer2_url = "https://conquer2.herokuapp.com/"
conquer2_url = "http://localhost:8080/"

class update_message:
    def __init__(self, dct):
        self.troops:int = dct["Troops"]
        self.type:str = dct["Type"]
        self.player:str = dct["Player"]
        self.country:str = dct["Country"]

def make_action(troops: int, action_type: str, src: str, dest: str):
    return f"{{\"Troops\": {troops}, \"ActionType\": \"{action_type}\", \"Src\": \"{src}\", \"Dest\": \"{dest}\"}}"
class conquer2_adapter:
    event_loop = asyncio.get_event_loop()
    players = []

    owners_lock = asyncio.Lock()
    owners = {}
    troops_lock = asyncio.Lock()
    troops = 0
    countries_lock = asyncio.Lock()
    countries = {}

    send_lock = asyncio.Lock()
    action = None #The message to be sent
    sent = asyncio.Semaphore(value=1)

    def __init__(self, username: str, password: str, code: str):
        self.username = username
        self.password = password
        self.code = code

        self.start_event = asyncio.Event()
        self.end_event = asyncio.Event()

        response = post(conquer2_url+"join", {"username": username, "password": password, "id": code})
        if response.status_code != 200:
            raise ConnectionRefusedError("Unable to login to game")
    
    async def manage_connection(self):
        url = conquer2_url.replace("http", "ws") + f"game/{self.code}/ws"
        async with websockets.connect(url, extra_headers={"Cookie": f"username={self.username}; password={self.password}"}) as websocket:
            self.websocket = websocket
            await websocket.send(make_action(0, "imreadym9", "", ""))
            while True:
                await self._send(websocket)
                await self._recv(websocket)

    async def _send(self, websocket):
        # if self.exit
        #send a message if one's ready
        with self.send_lock:
            if self.action != None:
                await websocket.send(self.action)
                self.sent.release() 

    async def _recv(self, websocket):
        msg = await websocket.recv()
        msg = json.loads(msg)
        if msg.type == "updateCountry":
            return False
        elif msg.type == "updateTroops":
            return False
        elif msg.type == "readyPlayer":
            return False
        elif msg.type == "newPlayer":
            return False
        elif msg.type == "start":
            self.start_event.set()
            return False
        elif msg.type == "won":
            self.end_event.set()
            return True
        else:
            raise ValueError("Unknown message received")

    def send_command(self, action):
        ...

    
    def close(self):
        ...

c = conquer2_adapter("Akshat", "asdf", "001f91")
# c.run()
print("done?")