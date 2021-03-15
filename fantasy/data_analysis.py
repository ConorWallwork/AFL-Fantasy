
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np


from player import *
from pulp import *

def linearOptimisation(players):

    player = [p.name for p in players]
    value = {p.name: p.value for p in players}
    price = {p.name: p.price for p in players}
    defe = {p.name: 1 if p.position == "Defender" else 0 for p in players}
    mid = {p.name: 1 if p.position == "Midfield" else 0 for p in players}
    forw = {p.name: 1 if p.position == "Forward" else 0 for p in players}
    ruk = {p.name: 1 if p.position == "Ruck" else 0 for p in players}

    prob = LpProblem("Fantasy Football",LpMaximize)
    player_vars = LpVariable.dicts("Players",player,0,1,LpBinary)

    prob += lpSum([value[i]*player_vars[i] for i in player]), "Total Cost"

    prob += lpSum([price[i] * player_vars[i] for i in player]) <= 10800000, "Total Cost"
    prob += lpSum([ruk[i] * player_vars[i] for i in player]) == 2, "Total Rucks"
    prob += lpSum([defe[i] * player_vars[i] for i in player]) == 6, "Total Defenders"
    prob += lpSum([mid[i] * player_vars[i] for i in player]) == 8, "Total Mids"
    prob += lpSum([forw[i] * player_vars[i] for i in player]) == 6, "Total Forwards"

    status = prob.solve()

    for name in player:
        if( player_vars[name].value() == 1):
            for p in players:
                if(p.name == name):
                    print(p.name + ", " + p.position + ", "+str(p.value))

    #    if(selected == 1):
    #        print(name)
    #return status


def main():

    print("hello world")
    players = getPlayersFromFile("players2019.csv", True)

    print(linearOptimisation(players))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
