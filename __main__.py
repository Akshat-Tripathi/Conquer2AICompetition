from game_utils.special_game import special_game
from game_utils.util import load_countries, load_probs
from game_utils.human_agent import human_agent
from game_utils.random_agent import random_agent
from game_utils.logger import logger
from game_utils.timer import turn_timer

from random import seed
from os import listdir
seed(124)

n_agents = 6

import time

#PRE the agents and game have already been initialised
def play(agents, logging, output=None):
    done = False
    i = 0
    turns = 0
    while not done:
        try:
            agent = agents[i]
            action = agent.step()
            done = agent.game.take_action(action, i)
            
            
            if output is not None:
                output.send(action, i)
            
            agent.game.timer.tick()
            i += 1
            turns += 1
            i %= len(agents)
            print(agent.game.players)
            logging.log(agent.game.state)
        except KeyboardInterrupt:
            if input("Save game? (Y | N)\n").upper() == "N":
                exit(0)
            return

from game_utils.connection.conquer import conquer_adapter
if __name__ == "__main__":
    t = turn_timer(60)
    game_map, _ = load_countries("game_utils/conquer_map.txt")
    g = special_game(game_map, n_agents, t, 1, 10)
    c = conquer_adapter(g)
    log = logger()
    agents = [random_agent(g, i) for i in range(n_agents)]
    c.init_game()

    play(agents, log, c)
    n = len(listdir("./games"))
    log.flush(f"./games/minimax{n}")
    print(f"saved game as minimax{n}")