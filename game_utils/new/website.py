from requests import post
import asyncio
import json
import websockets


conquer2_url = "https://conquer2.herokuapp.com/"

class update_message:
    def __init__(self, dct):
        self.troops:int = dct["Troops"]
        self.type:str = dct["Type"]
        self.player:str = dct["Player"]
        self.country:str = dct["Country"]

action_types = ["deploy", "attack", "move", "assist", "donate"]

def make_action(troops: int, action_type: str, src: str, dest: str):
    return f"{{\"Troops\": {troops}, \"ActionType\": \"{action_type}\", \"Src\": \"{src}\", \"Dest\": \"{dest}\"}}"

class conquer2_adapter:
    players = {}

    troops_lock = asyncio.Lock()
    troops = 0
    countries_lock = asyncio.Lock()
    countries = []

    actions = asyncio.Queue(maxsize=5)

    def __init__(self, username: str, password: str, code: str, idx_to_country_name):
        self.username = username
        self.password = password
        self.code = code

        self.idx_to_country_name = idx_to_country_name
        self.country_name_to_idx = dict([(idx_to_country_name[i], i) for i in range(len(idx_to_country_name))])

        self.start_event = asyncio.Event()
        self.end_event = asyncio.Event()

        response = post(conquer2_url+"join", {"username": username, "password": password, "id": code})
        if response.status_code != 200:
            raise ConnectionRefusedError("Unable to login to game")
    
    
    async def manage_connection(self):
        url = conquer2_url.replace("http", "ws") + f"game/{self.code}/ws"
        self.websocket = await websockets.connect(url, extra_headers={"Cookie": f"username={self.username}; password={self.password}"})
        await self.websocket.send(make_action(0, "imreadym9", "", ""))
        asyncio.ensure_future(self._send(self.websocket))
        asyncio.ensure_future(self._recv(self.websocket))

    async def _send(self, websocket):
        while True:
            action = await self.actions.get()
            await websocket.send(action)

    async def _recv(self, websocket):
        while True:
            msg = await websocket.recv()
            msg = update_message(json.loads(msg))
            if msg.type == "won":
                print("won")
                self.end_event.set()
                return True

            if msg.type == "updateCountry":
                with await self.countries_lock:
                    self.countries += [(self.country_name_to_idx[msg.country], 
                        msg.troops, msg.player)]

            elif msg.type == "updateTroops":
                with await self.troops_lock:
                    self.troops += msg.troops
            
            elif msg.type == "readyPlayer":
                pass
            elif msg.type == "newPlayer":
                self.players[msg.player] = len(self.players)
            elif msg.type == "start":
                print("started")
                self.start_event.set()
            else:
                raise ValueError("Unknown message received")

    async def send_command(self, action):
        action_type, src, dest, troops = action
        if action_type == 5:
            return
        act = make_action(troops, action_types[action_type],
            self.idx_to_country_name[src], self.idx_to_country_name[dest])
        await self.actions.put(act)
            

    async def get_n_players(self):
        await self.start_event.wait()
        return len(self.players)

    async def get_state(self):
        await self.start_event.wait()
        with await self.countries_lock:
            countries = self.countries.copy()
            self.countries = []
        with await self.troops_lock:
            troops = self.troops
        return troops, list(map(lambda country: (country[0], country[1], self.players[country[2]]), countries))