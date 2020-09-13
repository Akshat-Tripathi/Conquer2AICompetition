from basegame import basegame
from util import default_rng
import numpy as np

class game(basegame):

    #This version of attack is the same as the actual Conquer2 attack, but not the same as "autoattack like it's 'nam"
    def attack(self, src, dest, player):
        dest_player = np.argmax(self.state[dest]) 

        source = self.state[src, player]
        destination = self.state[dest, dest_player]

        deltaSrc, deltaDest = 0, 0
        
        if destination != 0:
            deltaSrc, deltaDest = default_rng(source, destination, 1)

        self.state[dest, dest_player] += deltaSrc
        self.state[dest, dest_player] += deltaDest

        source = self.state[src, player]
        destination = self.state[dest, dest_player]

        if destination < 0:
            deltaDest -= destination
            self.state[dest, dest_player] = 0
        
        if self.state[dest, dest_player] == 0 and source > 0:
            #Conquered
            self.state[dest, dest_player] = 1
            self.state[src, player] -= 1

            if np.sum(self.state[:, dest_player]) == 0 and destination != 0:
                self.alive_players.remove(dest_player)
            if np.count_nonzero(self.state[:, player]) == len(self.graph):
                return True

    def valid_attacks(self, player):
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
        return np.hstack((np.ones((len(attacks), 1)), attacks))
