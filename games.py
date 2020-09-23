from .util import default_rng
import numpy as np
import random

#An enum to represent special troop requests
all_troops = 0
split_troops = -1

class games:
    def __init__(self, graph, num_players, timer, 
                validate_actions=False, initial_countries=1,
                initial_troops=10):
        self.graph = graph
        self.num_players = num_players
        self.win_countries = len(graph)
        self.timer = timer
        
        self.validate_actions = validate_actions
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
                if not np.sum(self.ownership[index]):
                    self.set_owner(index, i)
                    countries -= 1

        self.dead_players = []

        self.players = [{
            "troops": self.initial_troops,
            "countries": self.initial_countries
        } for i in range(len(self.num_players))]

    def set_owner(self, country, player):
        self.ownership[country] = player + 1
    
    def get_owner(self, country):
        return self.ownership[country] - 1
    
    def _preprocess_action(self, action, player):
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


    
    def attack(self, src, dest, player):
        src = int(src)
        dest = int(dest)
        srcTroops = self.state[src]
        destTroops = self.state[dest]

        deltaSrc, deltaDest = 0, 0

        if destTroops != 0:
            deltaSrc, deltaDest = default_rng(srcTroops, destTroops, 1)
        
        return self.simulate_attack(src, dest, player, deltaSrc, deltaDest)
    
    def simulate_attack(self, src, dest, player, deltaSrc, deltaDest):
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

    def deploy(self, dest, troops, player):
        troops = self._preprocess_action([0, 0, 0, troops], player)
        self.state[dest] += troops
        self.players[player]["troops"] -= troops
        return False
    
    def move(self, src, dest, troops, player):
        troops = self._preprocess_action([2, src, 0, troops], player)
        self.state[dest] += troops
        self.state[src] -= troops
        return False
    
    def assist(self, src, dest, troops, player):
        ...
    
    def donate(self, player, recepient, troops):
        ...



    def _validate_attack(self, src, dest, player):
        ...
    
    def _validate_deploy(self, dest, troops, player):
        ...
    
    def _validate_move(self, src, dest, troops, player):
        ...
    
    def _validate_assist(self, src, dest, troops, player):
        ...
    
    def _validate_donate(self, player, recepient, troops):
        ...
    

    def _update_troops(self):
        ...



    def get_valid_actions(self, player):
        ...

    def _valid_attacks(self, src, dest, player):
        ...
    
    def _valid_deployments(self, dest, troops, player):
        ...
    
    def _valid_moves(self, src, dest, troops, player):
        ...
    
    def _valid_assists(self, src, dest, troops, player):
        ...
    
    def _valid_donationss(self, player, recepient, troops):
        ...