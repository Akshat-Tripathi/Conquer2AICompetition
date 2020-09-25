from .agent import agent

import numpy as np

class human_agent(agent):

    def step(self):
        if self.player not in self.game.dead_players:
            action = self._select_action()
        return action
    
    def _select_action(self):
        troops = self.game.players[self.player]["troops"]
        print(f"Player {self.player} has {troops} troops")
        
        for (i, (troops, owner)) in enumerate(zip(self.game.state, self.game.ownership)):
            print(f"Country: {i} has {troops} troops and is owned by {owner}")

        action_type = int(input("Action type?\nDeploy: 0\nAttack: 1\nMove: 2\nSkip: 3\n"))
        src = int(input("Src\n"))
        dest = int(input("Dest\n"))
        troops = int(input("Troops\n"))
        
        action = [action_type, src, dest, troops]
        valid_actions = self.game.get_valid_actions(self.player)
        if not any(np.array_equal(x, action) for x in valid_actions):
            print("Invalid action")
            self._select_action()
            
        return action