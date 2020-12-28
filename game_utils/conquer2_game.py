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
    def __init__(self, n_players: int, owners: List[:tuple[:str, :int]], initial_troops: int):
        game_map, tokens = load_countries("game_utils/conquer2_map.txt")
        super().__init__(game_map, n_players, dummy_timer(), 0, initial_troops)
        
        self.country_name_to_idx = {}
        for i in range(len(tokens)):
            self.country_name_to_idx[tokens[i]] = i
        
        for (country, player_idx) in owners:
            self.set_owner(self.country_name_to_idx[country], player_idx)