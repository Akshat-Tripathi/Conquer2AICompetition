import sys
import tempfile
import webbrowser
import numpy as np
from itertools import groupby

visualisation_file = sys.argv[1]
map_file = sys.argv[2]

def read_map(filepath):
    with open(filepath, "r") as file:
        tokens = list(filter(lambda s: s != "", set(file.read().replace("\n", " ").split(" "))))
        tokens.sort()
        world = []
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            countries = line[:-1].split(" ")
            for neighbour in countries[1:]:
                world += [f"{tokens.index(countries[0])} -> {tokens.index(neighbour)}"]
    return "; ".join(world)

def read_colours(filename):
    with open(filename) as file:
        return list(map(lambda s: s.replace("\n", ""), file.readlines()))

colours = read_colours("colours.txt")


def encode_state(state):
    owners = np.argmax(np.hstack((state, np.ones((len(state), 1)))), 1)
    encoded = []
    for j in range(len(owners)):
        owner = owners[j]
        colour = "#FFFFFF"
        troops = 0
        if owner != state.shape[1]:
            colour = colours[owner]
            troops = state[j, owner]
        encoded += [f"{j} [fillcolor=\"{colour}\" label={int(troops)}]"]
    return "; ".join(encoded)
        
states = np.load(visualisation_file)[::-1]
world = read_map(map_file)

graphs = [f"[\'digraph {{node [style=\"filled\"]; {encode_state(state)}; {world}}}\']," for state in states]

#This is the location of the first ; in each graph
insert_index = 33
label_turn = lambda s, i: s[:insert_index] + f" turn [label=\"Turn: {i}\"]" + s[insert_index:]

active_graphs = [label_turn(v, i) for i, v in enumerate(graphs) if i == 0 or v != graphs[i-1]]

formatted_string = "\n\t".join(active_graphs)

with open("template.html") as file:
    html = file.read().replace("[[ .graph ]]", formatted_string)

with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    url = 'file://' + f.name
    f.write(html)
webbrowser.open(url)