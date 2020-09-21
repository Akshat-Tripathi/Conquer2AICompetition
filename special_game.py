#special_game is a type of game which shpws special troop requests in valid_actions

from game import game, split_troops
import numpy as np

class special_game(game):

    def _insert_special_requests(self, actions, val):
        if actions is None:
            return None
        cpy = np.copy(actions)
        cpy = np.hstack((cpy, np.zeros((len(cpy), 1))))
        cpy[:, -1] = val
        return cpy

    def valid_actions(self, player):
        moves = self._valid_moves(player)
        deploys = self._valid_deploys(player)
        tup = (
            self._valid_attacks(player),
            moves,
            deploys,
            np.array([[3, 0, 0]])
        )
        split_troops_actions = np.vstack(i for i in map(lambda a: self._insert_special_requests(a, split_troops), [moves, deploys]) if i is not None)
        actions = np.vstack(i for i in tup if i is not None)
        return np.vstack((np.hstack((actions, np.zeros((len(actions), 1)))), split_troops_actions))