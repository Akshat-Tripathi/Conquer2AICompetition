from .agent import agent

from random import randint, seed

class random_agent(agent):

    def step(self):
        if self.player in self.game.dead_players:
            return [5, 0, 0, 0]
        valid_actions = self.game.get_valid_actions(self.player, [0, 1, 2, 5])
        action = valid_actions[randint(0, len(valid_actions) - 1)]
        return action