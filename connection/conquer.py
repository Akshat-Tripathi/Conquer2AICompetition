import asyncio
import websockets
import requests
import os
import numpy as np
import json
import time

from ..game import game
from .selenium_hosting import driver, set_country

ip_port = "192.168.1.2:8080"
class conquer:
    def __init__(self, game):
        #get players and their colours
        self.game = game
        self.player_code_colours = []
        self.colour_indices = {}
        with open(os.path.dirname(os.path.abspath(__file__)) + "\\accounts.txt", "r") as file:
            lines = file.read().split("\n")
            lines.sort()
            for i in range(len(lines)):
                code, colour = lines[i].split(";")
                self.player_code_colours.append((code, colour))
                self.colour_indices[colour] = i 
        
        with open(os.path.dirname(os.path.abspath(__file__)) + "\\countries.txt", "r") as file:
            countries = file.read().split("\n")
            countries = list(filter(lambda s: s != "", set(countries)))
            countries.sort()
            countries = list(map(lambda s: s.split(";")[0], countries))
            self.countries = countries
    
    def init_game(self):
        for i in range(len(self.countries)):
            self._set(i)

    def send(self, action, player):
        action_type, src, dest, _ = action
        if action_type == 0:
            set_country("PO", self.game.players[player]["troops"], "#ffffff")
        else:
            self._set(src)
            self._set(dest)
    
    def _set(self, country):
        troops = self.game.state[country]
        owner = self.game.get_owner(country)
        if owner == -1:
            return
        set_country(self.countries[country], troops, self.player_code_colours[owner][1])
