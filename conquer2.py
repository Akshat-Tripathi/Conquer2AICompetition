import asyncio
from .game_utils.new.website import conquer2_adapter
from .game_utils.util import load_countries
from .game_utils.conquer2_game import conquer2_game
from .game_utils.random_agent import random_agent
from .game_utils.logger import logger
from os import sys

async def play(agent, logging):
    username, password, code = sys.argv[1:]
    game_map, tokens = load_countries("game_utils/game_utils/conquer2_map.txt")
    website = conquer2_adapter(username, password, code, tokens)
    await website.manage_connection()
    game = conquer2_game(await website.get_n_players(), game_map)
    print("starting")
    my_player = website.players[username]
    agent = agent(game, my_player)
    i = 0 #This is a nasty hack to get around the bug where state doesn't update properly
    while True:
        troops, countries = await website.get_state()
        game.set_stonks(my_player, troops)
        for country in countries:
            game.update_country(*country)
        
        await asyncio.sleep(0.1)
        if i % 2:
            action = agent.step()
            logging.log(game.state)
            await website.send_command(action)
        i += 1
        if website.end_event.is_set():
            loop.stop()
            break

if __name__ == "__main__":
    agent = random_agent
    loop = asyncio.get_event_loop()
    loop.run_until_complete(play(agent, logger()))