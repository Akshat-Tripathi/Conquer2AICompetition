from .agent import agent

import numpy as np

class human_agent(agent):

    def step(self):
        if self.player in self.game.alive_players:
            action = self._select_action()
        return action
    
    def _select_action(self):
        troops = self.game.players[self.player]
        print(f"Player {self.player} has {troops} troops")
        
        for (i, country) in enumerate(self.game.state):
            print(f"{i}: {country}")

        action_type = int(input("Action type?\nDeploy: 0\nAttack: 1\nMove: 2\nSkip: 3\n"))
        src = int(input("Src\n"))
        dest = int(input("Dest\n"))
        
        action = [action_type, src, dest, 0]
        if not any(np.array_equal(x, action) for x in self.game.valid_actions(self.player)):
            print("Invalid action")
            self._select_action()
            
        return action