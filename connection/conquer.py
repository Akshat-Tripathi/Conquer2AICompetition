import asyncio
import websockets
import requests
import os
import numpy as np
import json
import time

from ..game import game

ip_port = "192.168.1.2:8080"
class conquer:
    def __init__(self, game):
        self.game = game
        self.connections = []
        self.event_loop = asyncio.get_event_loop()

        #get players and their colours
        self.player_code_colours = []
        self.colour_indices = {}
        with open(os.path.dirname(os.path.abspath(__file__)) + "\\accounts.txt", "r") as file:
            lines = file.read().split("\n")
            lines.sort()
            for i in range(len(lines)):
                code, colour = lines[i].split(";")
                self.player_code_colours.append((code, colour))
                self.colour_indices[colour] = i

    
    def register_player(self, player_index):
        #get player code
        player_code, _ = self.player_code_colours[player_index]
        #listen to the player's websocket (add it to the event loop)
        self.event_loop.run_until_complete(self._connect(player_code))
    
    async def _connect(self, player_code):
        uri = f"ws://{ip_port}/ws/{player_code}"
        self.connections += [await websockets.connect(uri, extra_headers=[("cookie", f"id={player_code}")])]

    def init_game(self):
         #Parse the request and set the initial game state
        countries = requests.get(f"http://{ip_port}/static/initial/countries.txt").text.split("\n")
        countries = list(filter(lambda s: s != "", set(countries)))
        countries.sort()
        countries = list(map(lambda s: s.split(";"), countries))
        self.countries = countries
        self.game.state = np.zeros_like(self.game.state)
        for country in range(len(countries)):
            colour = countries[country][2]
            if colour not in self.colour_indices:
                continue
            owner = self.colour_indices[colour]
            if owner >= len(self.game.alive_players):
                continue
            self.game.state[country, owner] = 1
            self.send([0, owner, country, 1], owner)

    #Listens to a player's websocket
    def listen(self, ws, player):
        ...

    #format the action and add it to the event loop
    def send(self, action, player):
        ws = self.connections[player]
        self.event_loop.run_until_complete(self._send(action, player, ws))

    async def _send(self, action, player, ws):
        action_type, src, dest, troops = action
        src = int(src)
        dest = int(dest)
        troops = int(troops)
        if action_type == 3:
            return
        msg = {
                "Player": self.player_code_colours[player][0],
                "Src": self.countries[src][0],
                "Dest": self.countries[dest][0],
                "MoveType": 0,
                "NumSrc": 0,
                "NumDest": 0,
            }
        #0 is deploy, 1 is attack, 2 is move
        #send 0 for an attack, 1 for a donation and 2 for a movement - conquer.go
        if action_type == 1: #attack
            msg["MoveType"] = 0
        else:
            msg["MoveType"] = 2
            print(troops)
            if action_type == 0: #deploy
                msg["Src"] = "PO"
                troops = self.game._preprocess_troops(0, 0, player, troops)
            else: #move
                troops = self.game._preprocess_troops(src, 2, player, troops)
            print(troops)
            msg["NumSrc"] = -int(troops)
            msg["NumDest"] = int(troops)

        print(msg, action)
        try:
            await ws.send(json.dumps(msg))
        except websockets.exceptions.ConnectionClosedError:
            print("websocket bug")
            time.sleep(5)
            await self._connect(self.player_code_colours[player][0])
            await ws.send(json.dumps(msg))



print("Hi")