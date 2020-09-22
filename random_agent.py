from .agent import agent

from random import randint, seed

class random_agent(agent):

    def step(self):
        if self.player not in self.game.alive_players:
            return [3, 0, 0, 0]
        actions = self.game.valid_actions(self.player)
        action = actions[randint(0, len(actions) - 1)]
        return action