# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 14:29:46 2020

@author: Akshat
"""

from random import randint

def default_rng(attackers, defenders, times):
    da, dd = 0, 0
    temp_a = attackers
    temp_d = defenders
    while times > 0 and temp_a > 0 and temp_d > 0:
        da, dd = default_rng_helper(attackers, defenders)
        temp_a += da
        temp_d += dd
        times -= 1
    if temp_a < 0:
        return 0, temp_d - defenders
    return temp_a - attackers, temp_d - defenders

#PRE: defenders > 0
def default_rng_helper(attackers, defenders):
    attackers = max(attackers, 3)
    defenders = max(defenders, 2)

    attack = [0] * attackers
    defend = [0] * defenders

    for i in range(attackers):
        attack[i] = randint(0, 5)
    for i in range(defenders):
        defend[i] = randint(0, 5)

    attack.sort(reverse=True)
    defend.sort(reverse=True)

    n = min(attackers, defenders)

    attackers = 0
    defenders = 0

    for i in range(n):
        if attack[i] <= defend[i]:
            attackers -= 1
        else:
            defenders -= 1

    return attackers, defenders