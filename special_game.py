#special_game is a type of game which shpws special troop requests in valid_actions

from .game import game, split_troops
import numpy as np

def _set_array_last_column(array, value):
    array[:, -1] = value

#since 0 is already a special 
def _insert_special_requests(actions, vals):
    return np.vstack([actions] + [_set_array_last_column(np.copy(actions), val) for val in vals])

class special_game(game):

    def get_valid_moves(self, player: int):
        return _insert_special_requests(super().get_valid_moves(player), [split_troops])
    
    def get_valid_assists(self, player: int):
        return _insert_special_requests(super().get_valid_assists(player), [split_troops])
    
    def get_valid_deployments(self, player: int):
        return _insert_special_requests(super().get_valid_deployments(player), [split_troops])
    
    def get_valid_donations(self, player: int):
        return _insert_special_requests(super().get_valid_donations(player), [split_troops])