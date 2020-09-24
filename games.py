from .util import default_rng
import numpy as np
from collections import deque
import random

#An enum to represent special troop requests
all_troops = 0
split_troops = -1

class games:
    initial_countries = 1
    initial_troops = 10
    base_timer = 45

    def __init__(self, graph, num_players, validate_actions=False):
        self.graph = graph
        self.num_players = num_players
        self.win_countries = len(graph)
        self.simulated_actions = deque()

        self.take_action = self._take_action
        self.simulate_action = self._simulate_action
        if validate_actions:
            self.take_action = lambda a, p: self._take_action(a, p) if self._validate_action(a, p) else None
            self.simulate_action = lambda a, p: self._simulate_action(a, p) if self._validate_action(a, p) else None

        self.reset()

    def reset(self):
        self.timer = self.base_timer - 1
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

    def _timer_next(self, player):
        if player == 0:
            if self.timer == 0:
                old_players = np.copy(self.players)
                self.players += self._process_troops()
                self.timer = self.base_timer - 1
                return old_players
            self.timer -= 1

    def _preprocess_troops(self, country, action_type, player, troops):
        if action_type != 0: #deploy
            array = self.state[country]
            delta = 1
        else:
            array = self.players
            delta = 0
        if troops == all_troops:
            return array[player] - delta
        if troops == split_troops:
            return array[player] // 2
        return troops

    #This version of attack is the same as the actual Conquer2 attack, but not the same as "autoattack like it's 'nam"
    def attack(self, src, dest, player):
        dest_player = np.argmax(self.state[dest])

        source = self.state[src, player]
        destination = self.state[dest, dest_player]

        deltaSrc, deltaDest = 0, 0
        
        if destination != 0:
            deltaSrc, deltaDest = default_rng(source, destination, 1)

        return self._attack(src, dest, player, deltaSrc, deltaDest)        

    def deploy(self, dest, troops, player):
        troops = self._preprocess_troops(0, 0, player, troops)
        self.state[dest, player] += troops
        self.players[player] -= troops
    
    def move(self, src, dest, troops, player):
        troops = self._preprocess_troops(src, 2, player, troops)
        self.state[dest, player] += troops
        self.state[src, player] -= troops

    #deltaSrc and deltaDest are any negative numbers or 0
    def _attack(self, src, dest, player, deltaSrc, deltaDest):
        dest_player = np.argmax(self.state[dest])
        
        self.state[src, player] += deltaSrc
        self.state[dest, dest_player] += deltaDest

        source = self.state[src, player]
        destination = self.state[dest, dest_player]

        if destination < 0:
            deltaDest -= destination
            self.state[dest, dest_player] = 0
        
        if self.state[dest, dest_player] == 0 and source > 0:
            #Conquered
            self.state[dest, dest_player] = 0
            self.state[dest, player] = 1
            self.state[src, player] -= 1

            if np.sum(self.state[:, dest_player]) == 0 and destination != 0:
                self.alive_players.remove(dest_player)
            if np.count_nonzero(self.state[:, player]) == len(self.graph):
                return True
        return False
    
    def simulate_attack(self, src, dest, player, deltaSrc, deltaDest):
        src = int(src)
        dest = int(dest)
        old_players = self._timer_next(player)

        #Both saves are tuples of shape (save_type, dest, player, troops)
        #save_type = 0 is for player updates, and save_type = 1 is for country_updates
        old_player = np.argmax(self.state[dest])
        save1 = (1, src, player, self.state[src, player])
        save2 = (dest, old_player, self.state[dest, old_player])
        
        self._attack(src, dest, player, deltaSrc, deltaDest)
        
        self.simulated_actions.append((save1, save2, old_players))

    #Getters
    #This returns how many troops can be deployed
    def get_deploy_numbers(self, player):
        return self.players[player]
    
    #This returns how many troops can be moved from one country
    def get_move_troops(self, country, player):
        return self.state[country, player]

    #Validation
    def _validate_action(self, action, player):
        action_type, src, dest, troops = action
        if action_type == 1:
            return self._validate_attack(src, dest, player)

        if troops == all_troops or troops == split_troops:
            troops = 0
        
        if action_type == 0:
            return self._validate_deploy(dest, player, troops)
        if action_type == 2:
            return self._validate_move(src, dest, player, troops)
        return True
    
    def _validate_attack(self, src, dest, player):
        #check that the player owns the src and has more than 1 troop to attack
        if self.state[src, player] < 2:
            return False
        #check that the player doesn't own the destination
        if self.state[dest, player] != 0:
            return False
        return True
    
    def _validate_move(self, src, dest, player, troops):
        t = self.state[src, player]
        #check that the player has the troops to move
        if t <= troops or troops < 0:
            return False
        #check that the player owns the src
        if t == 0:
            return False
        #check that the player owns the destination
        if self.state[dest, player] == 0:
            return False
        return True
    
    def _validate_deploy(self, dest, player, troops):
        t = self.players[player]
        #check that the player has the troops to deploy
        if t < troops or troops < 0:
            return False
        #check that the player owns the destination
        if self.state[dest, player] == 0:
            return False
        return True
        
    def _take_action(self, action, player):
        action_type, src, dest, troops = action
        src = int(src)
        dest = int(dest)
        
        if action_type == 0:
            self.deploy(dest, troops, player)
        elif action_type == 1:
            return self.attack(src, dest, player)
        elif action_type == 2:
            self.move(src, dest, troops, player)
        
        self._timer_next(player)
        return False
        
    def _process_troops(self):
        return (3 + np.count_nonzero(self.state, 0) / 3).astype(int)

    #All valid_ getters will return a numpy array of size 3 x valid_actions
    #0 represents the action type, 1 the src, 2 the dest
    #0 -> Deploy, 1 -> Attack, 2 -> Move, 3 -> No-op
    #PRE: the player is still alive

    def valid_actions(self, player):
        tup = (
            self._valid_attacks(player),
            self._valid_moves(player),
            self._valid_deploys(player),
            np.array([[3, 0, 0]])
        )
        actions = np.vstack(i for i in tup if i is not None)
        return np.hstack((actions, np.zeros((len(actions), 1))))

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

    #Simulators

    #PRE: the action is valid
    def _simulate_action(self, action, player):
        action_type, src, dest, troops = action
        src = int(src)
        dest = int(dest)
        old_players = self._timer_next(player)

        #Both saves are tuples of shape (save_type, dest, player, troops)
        #save_type = 0 is for player updates, and save_type = 1 is for country_updates
        save1 = (1, src, player, self.state[src, player])
        save2 = (dest, player, self.state[dest, player])
        won = False

        if action_type == 0:
            save1 = (0, 0, player, self.players[player])
            self.deploy(dest, troops, player)
        elif action_type == 1:
            old_player = np.argmax(self.state[dest])
            save2 = (dest, old_player, self.state[dest, old_player])
            won = self.attack(src, dest, player)
        elif action_type == 2:
            self.move(src, dest, troops, player)
        else:
            return False
        self.simulated_actions.append((save1, save2, old_players))
        return won
    
    def rollback_action(self):
        save1, save2, old_players = self.simulated_actions.pop()
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
        if player1 == 0:
            self.timer += 1
            self.timer %= self.base_timer
        if type(old_players) != type(None):
            self.players = old_players

    def __str__(self):
        return str((self.state.__str__(), self.players.__str__()))

    def __repr__(self):
        return self.state.__repr__()