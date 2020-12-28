from requests import post, get
# from websockets import send, recv
import asyncio
import json
import websockets


# conquer2_url = "https://conquer2.herokuapp.com/"
conquer2_url = "http://localhost:8080/"

def make_action(troops: int, action_type: str, src: str, dest: str):
    return f"{{\"Troops\": {troops}, \"ActionType\": \"{action_type}\", \"Src\": \"{src}\", \"Dest\": \"{dest}\"}}"
class conquer2_adapter:
    event_loop = asyncio.get_event_loop()

    def __init__(self, username: str, password: str, code: str):
        self.username = username
        self.password = password
        self.code = code

        response = post(conquer2_url+"join", {"username": username, "password": password, "id": code})
        if response.status_code != 200:
            raise ConnectionRefusedError("Unable to login to game")
    
    def run(self):
        async def loop():
            url = conquer2_url.replace("http", "ws") + f"game/{self.code}/ws"
            print(url)
            async with websockets.connect(url, extra_headers={"Cookie": f"username={self.username}; password={self.password}"}) as websocket:
                self.websocket = websocket
                await websocket.send(make_action(0, "imreadym9", "", ""))
                print("sent")
                while 1:
                    msg = await websocket.recv()
                    print(f"< {msg}")
        self.event_loop.run_until_complete(loop())
            

    def send_command(self, action):
        ...

    def get_state(self):
        ...
    
    def close(self):
        ...

c = conquer2_adapter("Akshat", "asdf", "001f91")
c.run()