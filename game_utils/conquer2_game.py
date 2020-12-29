from typing import List
from .special_game import special_game
from .util import load_countries
#This is the game that will be used for the competition
#The differences between this and special_game are not important
#Basically it allows the initial state to be set externally
#Note trying to change this will not actually affect the game on the server so
#hacking it won't actually do you any good

class dummy_timer:
    def add_event(self, _):
        pass
    
    def reset(self):
        pass
    
    def tick(self):
        pass

class conquer2_game(special_game):
    def __init__(self, n_players: int, game_map):
        super().__init__(game_map, n_players, dummy_timer(), 0, 0)
    
    def set_troops(self, player, troops):
        self.players[player]["troops"] = troops
    
    def update_country(self, country, troops, player):
        self.state[country] += troops
        self.set_owner(country, player)