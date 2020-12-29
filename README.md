#Conquer2 AI Competition
---

## What to do
You'll be creating a bot which will eventually play [Conquer2](https://github.com/Akshat-Tripathi/conquer2) against both other players and other players' bots. This repo contains several tools and helper code to make developing a bot player easier.

## Rules
1. Bots will take a maximum of 1 action per second even if the action is invalid
2. The creators of the bots will be barred from playing in games where their own bot is playing

### Conquer2 Rules
You can choose 1 of 5 types of action:
1. Attacks
    a. You must have more than 1 troop in the country you're attacking from
    b. You cannot own the country you are attacking
<br>

2. Movements
    a. You must move less than the number of troops in the source country
    b. You must own both the source and destination countries
<br>

3. Donations
    a. You can donate stonks to any player, dead or alive
    b. You cannot donate more stonks than you own
<br>

4. Buys (aka deploys)
    a. You must own the destination country
    b. You cannot use more stonks than you own
<br>


5. Assists
    a. You must move less than the number of troops in the source country
    b. You must own the source country but not the destination country

---

## Documentation

#### Actions
Actions are represented as tuples of size 4 with the following format:
`(action_type, src, dest, troops)`

<u>Action type</u>
There are 6 different types of action
<li> 0: Deploy (buy), ignores the value of src
<li> 1: Attack, ignores the value of troops
<li> 2: Move
<li> 3. Assist
<li> 4. Donate, ignores the value of src
<li> 5. Do nothing
</li>
<br>

<u>Src/Dest</u>
These are integers which represent which country to (move/assist) from and which country to (move/assist/deploy) to.
When donating, the other player's number is stored in dest

<u>Troops</u>
Troops represent the number of troops to be (moved/deployed/used to assist).
If troops is equal to 0, then all available troops/stonks will be used.
If troops is equal to -1, then half of the available troops/stonks will be used

#### Game
The [game](https://github.com/Akshat-Tripathi/Conquer2AICompetition/blob/main/game.py) class provides the basic implementation of a game.

```py
def __init__(self, graph, num_players, timer, initial_countries=1, initial_troops=10):
```
graph is an adjacency matrix used to store the map. 
timer represents a timer object.

The game represents the number of troops in each country in the state field, which is a numpy array with shape `(number_of_countries,)`

The game represents ownership in a similar array, but it is highly recommenended that you use the helper methods defined below.

##### Methods
```py
#Used to change who owns particular countries
set_owner(self, country, player)
get_owner(self, country) #returns -1 if noone owns the country
```

When you want to take an action, use the following.
```py
#Returns whether or not the action won the game
take_action(self, action, player)

attack(self, src, dest, player)

#Simulate attack performs an attack with the specified result
#Ie you can simulate a dice roll
simulate_attack(self, src, dest, player, deltaSrc, deltaDest)

deploy(self, dest, troops, player)
move(self, src, dest, troops, player)
assist(self, src, dest, troops, player)
donate(self, player, recepient, troops)
```
All the above methods return whether or not an action won the game, but only attacks can win games.
NB: None of the above validate actions, if you want to make sure that your action is valid, use the following.
```py
take_valid_action(self, action, player)
```

If you want to get all the valid actions use the following methods.
```py
#By default action_types covers all action types, change it if you want different action types
get_valid_actions(self, player, action_types)

get_valid_attacks(self, player):
get_valid_deployments(self, player):
get_valid_moves(self, player):
get_valid_assists(self, player):
get_valid_donations(self, player):
```

#### Agent
The [agent](https://github.com/Akshat-Tripathi/Conquer2AICompetition/blob/main/agent.py) class is what you should subclass when making your bot. You must override the `step` method.
Agents have games, and a unique player number, all agents will share the same game object.

Here's the implementation of the random_agent defined [here](https://github.com/Akshat-Tripathi/Conquer2AICompetition/blob/main/random_agent.py)
```py
from .agent import agent

from random import randint, seed

class random_agent(agent):

    def step(self):
        if self.player in self.game.dead_players:
            return [5, 0, 0, 0]
        valid_actions = self.game.get_valid_actions(self.player, [0, 1, 2, 5])
        action = valid_actions[randint(0, len(valid_actions) - 1)]
        return action
```
The random agent first checks if it is dead, and if so, it does nothing, otherwise it gets a list of valid actions, and selects one action at random and then returns it. When making a bot, you should override the step method to return the action you wish to take.

### Tools
The best way to visualise an agent on the Conquer map is to use [conquer.py](https://github.com/Akshat-Tripathi/Conquer2AICompetition/blob/main/connection/conquer.py)

Here's an example of its use
```py
from game_utils.connection.conquer import conquer
g = game(...)
visualisation = conquer(g)
#Add agents to the game

c.init_game()

c.send(action, player)
```