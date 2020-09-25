from typing import List
from .util import default_rng
import numpy as np
import random

#An enum to represent special troop requests
all_troops = 0
split_troops = -1

_validate_actions = False

def set_validate_actions(val: bool):
    _validate_actions = val

class game:
    def __init__(self, graph, num_players, timer, 
                initial_countries=1, initial_troops=10):
        self.graph = graph
        self.num_players = num_players
        self.win_countries = len(graph)
        self.timer = timer
        self.timer.add_event(self._update_troops)
        
        self.initial_countries = initial_countries
        self.initial_troops = initial_troops

        self.reset()
    
    def reset(self):
        self.timer.reset()

        #state represents how many troops each country has
        self.state = np.zeros((self.win_countries,))
        #ownership represents who owns which country (player + 1)
        self.ownership = np.zeros((self.win_countries,))
        
        for i in range(self.num_players):
            countries = self.initial_countries
            while countries:
                index = random.randint(0, self.win_countries - 1)
                if not self.ownership[index]:
                    self.set_owner(index, i)
                    countries -= 1

        self.dead_players = []

        self.players = [{
            "troops": self.initial_troops,
            "countries": self.initial_countries
        } for i in range(self.num_players)]

    def set_owner(self, country: int, player: int):
        self.ownership[country] = player + 1
    
    def get_owner(self, country: int) -> int:
        return self.ownership[country] - 1
    
    def get_countries_owned_by(self, player: int) -> List[int]:
        return np.argwhere(self.ownership == player + 1)
    
    def get_countries_not_owned_by(self, player) -> List[int]:
        return np.argwhere(self.ownership != player + 1)

    def _preprocess_action(self, action, player: int):
        action_type, src, _, troops = action
        if action_type == 0: #deploy
            current_troops = self.players[player]["troops"]
            delta = 0
        else: #move
            current_troops = self.state[src]
            delta = 1
        if troops == all_troops:
            return current_troops - delta
        if troops == split_troops:
            return current_troops // 2
        return troops


    def take_action(self, action, player: int) -> bool:
        action_type, src, dest, _ = action
        troops = self._preprocess_action(action, player)

        if action_type == 0:
            return self.deploy(dest, troops, player)
        elif action_type == 1:
            return self.attack(src, dest, player)
        elif action_type == 2:
            return self.move(src, dest, troops, player)
        elif action_type == 3:
            return self.assist(src, dest, troops, player)
        elif action_type == 4:
            return self.donate(player, dest, troops)
        return False
    
    def attack(self, src: int, dest: int, player) -> bool:
        srcTroops = self.state[src]
        destTroops = self.state[dest]

        deltaSrc, deltaDest = 0, 0

        if destTroops != 0:
            deltaSrc, deltaDest = default_rng(srcTroops, destTroops, 1)
        
        return self.simulate_attack(src, dest, player, deltaSrc, deltaDest)
    
    def simulate_attack(self, src, dest, player, deltaSrc, deltaDest) -> bool:
        srcTroops = self.state[src] + deltaSrc
        destTroops = self.state[dest] + deltaDest

        won = False
        #player has conquered dest
        if destTroops <= 0 and srcTroops > 1:
            destTroops = 1
            srcTroops -= 1

            #change ownership
            dest_player = self.get_owner(dest)
            self.set_owner(dest, player)
            self.players[player]["countries"] += 1
            self.players[dest_player]["countries"] -= 1

            if self.players[dest_player]["countries"] == 0:
                self.dead_players += [dest_player]
            if self.players[player]["countries"] == self.win_countries:
                won = True
        
        self.state[dest] = destTroops
        self.state[src] = srcTroops
        return won

    def deploy(self, dest: int, troops: int, player: int) -> bool:
        troops = self._preprocess_action([0, 0, 0, troops], player)
        self.state[dest] += troops
        self.players[player]["troops"] -= troops
        return False
    
    def move(self, src: int, dest: int, troops: int, player: int) -> bool:
        troops = self._preprocess_action([2, src, 0, troops], player)
        self.state[dest] += troops
        self.state[src] -= troops
        return False
    
    def assist(self, src: int, dest: int, troops: int, player: int) -> bool:
        return self.move(src, dest, troops, player)
    
    def donate(self, player: int, recepient: int, troops: int) -> bool:
        troops = self._preprocess_action([0, 0, 0, troops], player)
        self.players[recepient]["troops"] -= troops
        self.players[player]["troops"] -= troops
        return False


    def take_valid_action(self, action, player: int) -> bool:
        action_type, src, dest, _ = action
        troops = self._preprocess_action(action, player)

        if action_type == 0:
            if self._validate_deploy(dest, troops, player):
                return self.deploy(dest, troops, player)
        elif action_type == 1:
            if self._validate_attack(src, dest, player):
                return self.attack(src, dest, player)
        elif action_type == 2:
            if self._validate_move(src, dest, troops, player):
                return self.move(src, dest, troops, player)
        elif action_type == 3:
            if self._validate_assist(src, dest, troops, player):
                return self.assist(src, dest, troops, player)
        elif action_type == 4:
            if self._validate_donate(player, dest, troops):
                return self.donate(player, dest, troops)
        return False

    def _validate_attack(self, src: int, dest: int, player: int) -> bool:
        #check that the player owns the src
        if self.get_owner(src) != player:
            return False
        #check that the player doesn't own the dest
        if self.get_owner(dest) == player:
            return False
        #check that the player has enough troops to attack
        if self.state[src] < 2:
            return False
        return True
            
    def _validate_deploy(self, dest: int, troops: int, player: int) -> bool:
        t = self.players[player]["troops"]
        #check that the player has the troops to deploy
        if t < troops or troops < 0:
            return False
        #check that the player owns the destination
        if self.get_owner(dest) != player:
            return False
        return True
    
    def _validate_move(self, src: int, dest: int, troops: int, player: int) -> bool:
        t = self.state[src]
        #check that the player has the troops to move
        if t <= troops or troops < 0:
            return False
        #check that the player owns the src
        if self.get_owner(src) != player:
            return False
        #check that the player owns the dest
        if self.get_owner(dest) != player:
            return False
        return True
    
    def _validate_assist(self, src: int, dest: int, troops: int, player: int) -> bool:
        t = self.state[src]
        #check that the player has the troops to move
        if t <= troops or troops < 0:
            return False
        #check that the player owns the src
        if self.get_owner(src) != player:
            return False
        #check that the player doesn't the dest
        if self.get_owner(dest) == player:
            return False
        return True

    def _validate_donate(self, player: int, recepient: int, troops: int) -> bool:
        #can't donate to self
        if player == recepient:
            return False
        #must own enough troops
        t = self.players[player]["troops"]
        if t < troops or troops < 0:
            return False
        #can't donate to defeated players
        if recepient in self.dead_players:
            return False
        return True
    

    def _update_troops(self):
        return [(3 + self.players[player]["troops"]) / 3 for player in range(self.num_players)]

    def get_valid_actions(self, player: int, action_types=[0, 1, 2, 3, 4, 5]):
        actions = enumerate([
            self.get_valid_deployments(player),
            self.get_valid_attacks(player),
            self.get_valid_moves(player),
            self.get_valid_assists(player),
            self.get_valid_donations(player),
            np.array([5, 0, 0, 0])
        ])
        actions = filter(lambda k: k[0] in action_types, actions)
        
        return np.vstack(tuple(actions))


    def get_valid_attacks(self, player: int):
        my_countries = self.get_countries_owned_by(player)
        #can only attack if troops > 1
        my_countries = my_countries[self.state[my_countries] > 1]
        if len(my_countries) == 0:
            return []
        attackable_countries = self.get_countries_not_owned_by(player)
        if len(attackable_countries) == 0:
            return []
        
                #get all combos
        combos = np.array(np.meshgrid(my_countries, attackable_countries)).T.reshape(-1, 2)
        #Finds all valid neighbours
        neighbours = self.graph[combos[:, 0], combos[:, 1]]
        attacks = combos[np.nonzero(neighbours)]
        if len(attacks) == 0:
            return []
        attacks = np.hstack((np.ones((len(attacks), 1)), attacks))
        return np.hstack((attacks, np.zeros((len(attacks), 1)))).astype(int)
    
    def get_valid_deployments(self, player: int):
        if self.players[player]["troops"] == 0:
            return []
        countries = self.get_countries_owned_by(player)
        deployments = np.hstack((np.zeros((len(countries), 2)), countries))
        return np.hstack((deployments, np.zeros((len(deployments), 1)))).astype(int)

    def get_valid_moves(self, player: int):
        my_countries = self.get_countries_owned_by(player)
        #can only move if troops > 1
        my_countries = my_countries[self.state[my_countries] > 1]
        if len(my_countries) == 0:
            return []
        moveable_countries = self.get_countries_owned_by(player)
        if len(moveable_countries) == 0:
            return []
        
        #get all combos
        combos = np.array(np.meshgrid(my_countries, moveable_countries)).T.reshape(-1, 2)
        #Finds all valid neighbours
        neighbours = self.graph[combos[:, 0], combos[:, 1]]
        moves = combos[np.nonzero(neighbours)]
        if len(moves) == 0:
            return []
        move_actions = np.hstack((np.ones((len(moves), 1)) * 2, moves)) #[2, src, dest]
        return np.hstack((move_actions, np.zeros((len(move_actions), 1)))).astype(int)
    
    def get_valid_assists(self, player: int):
        my_countries = self.get_countries_owned_by(player)
        #can only assist if troops > 1
        my_countries = my_countries[self.state[my_countries] > 1]
        if len(my_countries) == 0:
            return []
        moveable_countries = self.get_countries_not_owned_by(player)
        if len(moveable_countries) == 0:
            return []
        
        #get all combos
        combos = np.array(np.meshgrid(my_countries, moveable_countries)).T.reshape(-1, 2)
        #Finds all valid neighbours
        neighbours = self.graph[combos[:, 0], combos[:, 1]]
        moves = combos[np.nonzero(neighbours)]
        if len(moves) == 0:
            return []
        move_actions = np.hstack((np.ones((len(moves), 1)) * 3, moves)) #[3, src, dest]
        return np.hstack((move_actions, np.zeros((len(move_actions), 1)))).astype(int)
    
    def get_valid_donations(self, player: int):
        if self.players[player]["troops"] == 0:
            return []
        return np.array([[4, 0, other_player, 0] for other_player in range(self.num_players)
                                                 if other_player != player and other_player not in self.dead_players]).astype(int)
    
    def copy(self, clas=None):
        if clas is None:
            clas = game
        g = clas(self.graph, self.num_players, self.timer, 0, 0)
        g.dead_players = self.dead_players.copy()
        g.state = np.copy(self.state)
        g.ownership = np.copy(self.ownership)
        g.players = self.players.copy()
        return g