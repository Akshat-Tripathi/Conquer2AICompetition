# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 14:16:15 2020

@author: Akshat
"""

import numpy as np
from .game import game

class simple_game(game):

    #this version of attack assumes 1 troop takes 1 troop
    def attack(self, src, dest, player):
        srcTroops = self.state[src]
        destTroops = self.state[dest]
        return self.simulate_attack(src, dest, player, srcTroops, destTroops)

    def _validate_attack(self, src, dest, player):
        if super()._validate_attack(src, dest, player):
            srcTroops = self.state[src]
            destTroops = self.state[dest]
            return srcTroops > destTroops
        return False

    def get_valid_attacks(self, player):
        attacks = super().get_valid_attacks(player)
        if attacks is None:
            return None
        return attacks[[self.state[int(attack[1])] > self.state[int(attack[2])] for attack in attacks]]