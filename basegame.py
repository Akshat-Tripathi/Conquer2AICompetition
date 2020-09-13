# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 14:16:15 2020

@author: Akshat
"""

import numpy as np
import random
from collections import deque

#Creates an adjacency matrix from the map
def load_countries(filepath):
    with open(filepath, "r") as file:
        tokens = list(filter(lambda s: s != "", set(file.read().replace("\n", " ").split(" "))))
        tokens.sort()
        world = np.zeros((len(tokens), len(tokens)))
        file.seek(0)
        for line in file.readlines():
            countries = line[:-1].split(" ")
            for neighbour in countries[1:]:
                world[tokens.index(countries[0]), tokens.index(neighbour)] = 1
    return world

class basegame():
    initial_countries = 1
    initial_troops = 10
    base_timer = 60

    def __init__(self, graph, num_players):
        self.graph = graph
        self.num_players = num_players
        self.win_countries = len(graph)
        self.simulated_actions = deque()

        self.reset()

    def reset(self):
        self.timer = self.base_timer
        self.state = np.zeros((self.win_countries, self.num_players))
        self.players = np.zeros((self.num_players))
        self.alive_players = list(range(self.num_players))
        #add initial players
        self.players[:] = self.initial_troops
        for i in range(self.num_players):
            countries = self.initial_countries
            while countries:
                index = random.randint(0, len(self.state) - 1)
                if not np.sum(self.state[index]):
                    self.state[index, i] = 1
                    countries -= 1

    def deploy(self, dest, player):
        self.state[dest, player] += self.players[player]
        self.players[player] = 0
    
    def move(self, src, dest, player):
        self.state[dest, player] += self.state[src, player] - 1
        self.state[src, player] = 1

    #this version of attack assumes 1 troop takes 1 troop
    def attack(self, src, dest, player):
        dest_player = np.argmax(self.state[dest]) 

        source = self.state[src, player]
        destination = self.state[dest, dest_player]

        delta = source - destination

        self.state[dest, dest_player] = 0
        if delta > 1:
            self.state[src, player] = delta - 1
            self.state[dest, player] = 1
            if np.sum(self.state[:, dest_player]) == 0 and destination != 0:
                self.alive_players.remove(dest_player)
            if np.count_nonzero(self.state[:, player]) == len(self.graph):
                return True
        else:
            self.state[src, player] = 1

    def take_action(self, action, player):
        if self.timer == 0:
            self.players += self._process_troops()
            self.timer = self.base_timer
        self.timer -= 1

        action_type, src, dest = action
        src = int(src)
        dest = int(dest)
        
        if action_type == 0:
            self.deploy(dest, player)
        elif action_type == 1:
            return self.attack(src, dest, player)
        elif action_type == 2:
            self.move(src, dest, player)
        return False
        
    def _process_troops(self):
        return (3 + np.count_nonzero(self.state, 0) / 3).astype(int)

    #All valid_ getters will return a numpy array of size 3 x valid_moves
    #0 represents the action type, 1 the src, 2 the dest
    #0 -> Deploy, 1 -> Attack, 2 -> Move, 3 -> No-op
    #PRE: the player is still alive

    #All deploys where the player has troops and countries
    def _valid_deploys(self, player):
        if self.players[player] == 0:
            return None
        countries = np.nonzero(self.state[:, player])[0]
        return np.vstack((np.zeros((2, len(countries))), countries)).T
    
    def _valid_attacks(self, player):
        #can only attack if troops > 1
        my_countries = np.nonzero(self.state[:, player] > 1)[0]
        if len(my_countries) == 0:
            return None
        attackable_countries = np.nonzero(self.state[:, player] == 0)[0]
        if len(attackable_countries) == 0:
            return None

        #get all combos
        combos = np.array(np.meshgrid(my_countries, attackable_countries)).T.reshape(-1, 2)
        #Finds all valid neighbours
        neighbours = self.graph[combos[:, 0], combos[:, 1]]
        attacks = combos[np.nonzero(neighbours)]
        if len(attacks) == 0:
            return None
        #srcTroops > destTroops + 1
        attacks = attacks[np.max(self.state[attacks[:, 0]]) - np.max(self.state[attacks[:, 1]]) > 1]
        if len(attacks) == 0:
            return None
        attacks = attacks[0]
        return np.hstack((np.ones((len(attacks), 1)), attacks))
    
    def _valid_moves(self, player):
        #can only move if troops > 1
        my_countries = np.nonzero(self.state[:, player] > 1)[0]
        if len(my_countries) == 0:
            return None
        moveable_countries = np.nonzero(self.state[:, player] > 0)[0]
        if len(moveable_countries) == 0:
            return None

        #get all combos
        combos = np.array(np.meshgrid(my_countries, moveable_countries)).T.reshape(-1, 2)
        #Finds all valid neighbours
        neighbours = self.graph[combos[:, 0], combos[:, 1]]
        moves = combos[np.nonzero(neighbours)]
        if len(moves) == 0:
            return None
        return np.hstack((np.ones((len(moves), 1)) * 2, moves))
    
    def valid_actions(self, player):
        tup = (
            self._valid_attacks(player),
            self._valid_moves(player),
            self._valid_deploys(player),
            np.array([[3, 0, 0]])
        )
        return np.vstack(i for i in tup if i is not None)

    #PRE: the action is valid
    def simulate_action(self, action, player):
        action_type, src, dest = action
        src = int(src)
        dest = int(dest)
        self.timer -= 1

        #Both saves are tuples of shape (save_type, dest, player, troops)
        #save_type = 0 is for player updates, and save_type = 1 is for country_updates
        save1 = (1, src, player, self.state[src, player])
        save2 = (dest, player, self.state[dest, player])
        
        if action_type == 0:
            save1 = (0, 0, player, self.players[player])
            self.deploy(dest, player)
        elif action_type == 1:
            old_player = np.argmax(self.state[dest])
            save2 = (dest, old_player, self.state[dest, old_player])
            self.attack(src, dest, player)
        elif action_type == 2:
            self.move(src, dest, player)
        else:
            return
        self.simulated_actions.append((save1, save2))
    
    def rollback_action(self):
        save1, save2 = self.simulated_actions.pop()
        save_type, dest1, player1, troops1 = save1
        dest2, player2, troops2 = save2
        if save_type == 0:
            self.players[player1] = troops1
        else:
            self.state[dest1, player1] = troops1
        
        self.state[dest2, player2] = troops2
        #Is attack
        if player1 != player2:
            if player2 not in self.alive_players:
                self.alive_players += [player2]
            self.state[dest2, player1] = 0
        
        #undo timer change
        self.timer += 1
        self.timer %= self.base_timer

    def __str__(self):
        return str((self.state.__str__(), self.players.__str__()))

    def __repr__(self):
        return self.state.__repr__()