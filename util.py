# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 14:29:46 2020

@author: Akshat
"""

from random import randint
import numpy as np
import itertools
import json

#Creates an adjacency matrix from the map
def load_countries(filename):
    with open(filename, "r") as file:
        tokens = list(filter(lambda s: s != "", set(file.read().replace("\n", " ").split(" "))))
        tokens.sort()
        world = np.zeros((len(tokens), len(tokens)))
        file.seek(0)
        for line in file.readlines():
            countries = line[:-1].split(" ")
            for neighbour in countries[1:]:
                world[tokens.index(countries[0]), tokens.index(neighbour)] = 1
    return world

def load_probs(filename):
    with open("probs.json") as file:
        raw = json.loads(file.read())
        str2tup = lambda s: tuple(int(i) for i in s.replace("(", "")
                                                   .replace(")", "")
                                                   .split(", "))
        convert_dict = lambda d: {str2tup(k):v for k, v in d.items()}

        return {str2tup(k):convert_dict(v) for k, v in raw.items()}

def calculate_probs():
    #Sets up all possible combos

    #A total of {attackers} must be lost
    #Attackers can lose upto {defenders} troops
    #Defenders can lose upto {attackers} troops
    combos_func = lambda attackers, defenders: {(-i, -j):0 for i in range(0, defenders + 1) 
                                                           for j in range(attackers - defenders, attackers + 1)
                                                           if i + j == attackers}
    probs = {}
    for defenders in range(1, 3):
        for attackers in range(2, 4):
            combos = combos_func(attackers, defenders)
            #Simulate all possible dice rolls for a particular scenario
            attacks = itertools.combinations_with_replacement(range(6), attackers)
            defences = list(itertools.combinations_with_replacement(range(6), defenders))
            for attack in attacks:
                attack = list(attack)
                attack.sort(reverse=True)
                for defence in defences:
                    # simulate a dice roll 
                    defence = list(defence)

                    defence.sort(reverse=True)
                    print(attack, defence)

                    dS, dD = 0, defenders - attackers #deltaSrc and deltaDest
                    for i in range(defenders):
                        result = attack[i] <= defence[i]
                        dS -= result
                        dD -= not result
                    
                    combos[(dS, dD)] += 1
            #Find probabilites rather than counts
            total = sum(combos.values())
            probs[str((attackers, defenders))] = {str(k): v /total for k, v in combos.items()}

    from os import system
    with open("temp.json", "w") as file:
        file.write(json.dumps(probs))
    system("python -m json.tool temp.json probs.json")
    system("erase temp.json")
    return probs

def default_rng(attackers, defenders, times):
    da, dd = 0, 0
    temp_a = attackers
    temp_d = defenders
    while times > 0 and temp_a > 0 and temp_d > 0:
        da, dd = default_rng_helper(int(attackers), int(defenders))
        temp_a += da
        temp_d += dd
        times -= 1
    if temp_a < 0:
        return 0, temp_d - defenders
    return temp_a - attackers, temp_d - defenders

#PRE: defenders > 0
def default_rng_helper(attackers, defenders):
    attackers = min(attackers, 3)
    defenders = min(defenders, 2)

    attack = [0] * attackers
    defend = [0] * defenders

    for i in range(attackers):
        attack[i] = randint(0, 5)
    for i in range(defenders):
        defend[i] = randint(0, 5)

    attack.sort(reverse=True)
    defend.sort(reverse=True)

    n = min(attackers, defenders)

    defenders = defenders - attackers
    attackers = 0

    for i in range(n):
        if attack[i] <= defend[i]:
            attackers -= 1
        else:
            defenders -= 1

    return attackers, defenders