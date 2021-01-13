from itertools import count
from typing import List
from .special_game import special_game
import numpy as np
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
    
    def set_stonks(self, player, troops):
        self.players[player]["troops"] = troops
    
    def update_country(self, country, troops, player):
        if self.get_owner(country) != player:
            self.set_owner(country, player)
            self.state[country] = troops
        else:
            if player == -1:
                self.state[country] = troops
            else:
                self.state[country] += troops

    def get_valid_actions(self, player: int, action_types):
        actions = super().get_valid_actions(player, action_types=action_types)
        troops = map(lambda action: self._preprocess_action(action, player), actions)
        return [(action[0], action[1], action[2], trps) for (action, trps) in zip(actions, troops)]
    
    def get_neighbours(self, country):
        return np.nonzero(self.graph[country])[0]

    def get_troops(self, country):
        return self.state[country]
    
    def get_stonks(self, player):
        return self.players[player]["troops"]