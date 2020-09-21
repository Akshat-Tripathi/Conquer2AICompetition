# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 14:16:15 2020

@author: Akshat
"""

import numpy as np
from game import game
from util import load_countries

class simple_game(game):

    # #this version of attack assumes 1 troop takes 1 troop
    # def attack(self, src, dest, player):
    #     dest_player = np.argmax(self.state[dest]) 

    #     source = self.state[src, player]
    #     destination = self.state[dest, dest_player]

    #     delta = source - destination

    #     self.state[dest, dest_player] = 0
    #     if delta > 1:
    #         self.state[src, player] = delta - 1
    #         self.state[dest, player] = 1
    #         if np.sum(self.state[:, dest_player]) == 0 and destination != 0:
    #             self.alive_players.remove(dest_player)
    #         if np.count_nonzero(self.state[:, player]) == len(self.graph):
    #             return True
    #     else:
    #         self.state[src, player] = 1

    # def _valid_attacks(self, player):
        #can only attack if troops > 1
        # my_countries = np.nonzero(self.state[:, player] > 1)[0]
        # if len(my_countries) == 0:
        #     return None
        # attackable_countries = np.nonzero(self.state[:, player] == 0)[0]
        # if len(attackable_countries) == 0:
        #     return None

        # #get all combos
        # combos = np.array(np.meshgrid(my_countries, attackable_countries)).T.reshape(-1, 2)
        # #Finds all valid neighbours
        # neighbours = self.graph[combos[:, 0], combos[:, 1]]
        # attacks = combos[np.nonzero(neighbours)]
        # if len(attacks) == 0:
        #     return None
        # #srcTroops > destTroops + 1
        # attacks = attacks[np.max(self.state[attacks[:, 0]]) - np.max(self.state[attacks[:, 1]]) > 1]
        # if len(attacks) == 0:
        #     return None
        # attacks = attacks[0]
        # return np.hstack((np.ones((len(attacks), 1)), attacks))
    
    def simulate_action(self, action, player):
        super().simulate_action(action, player)
    
    def take_action(self, action, player):
        return super().take_action(action, player)