
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np


from player import *
from pulp import *






def linearOptimisation(players, useBench, budget):

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

    nrucks = 0
    nmidfielders = 0
    nforwards = 0
    ndefenders = 0
    if(useBench):
        nrucks = 4
        nmidfielders = 10
        ndefenders = 8
        nforwards = 8
    else:
        nrucks = 2
        nmidfielders = 8
        ndefenders = 6
        nforwards = 6

    prob += lpSum([price[i] * player_vars[i] for i in player]) <= budget, "Total Cost"
    prob += lpSum([ruk[i] * player_vars[i] for i in player]) == nrucks, "Total Rucks"
    prob += lpSum([defe[i] * player_vars[i] for i in player]) == ndefenders, "Total Defenders"
    prob += lpSum([mid[i] * player_vars[i] for i in player]) == nmidfielders, "Total Mids"
    prob += lpSum([forw[i] * player_vars[i] for i in player]) == nforwards, "Total Forwards"





    status = prob.solve()

    for p in players:
        if player_vars[p.name].value() == 1:
            print(p.__dict__)


def linearOptimisationTrades(players, positives, negatives, budget, playersin, playersout):
    negatives_names = [p.name for p in negatives]
    positives_names = [p.name for p in positives]
    player = [p.name for p in players]

    value = {p.name: p.value for p in players}
    price = {p.name: p.price for p in players}

    positive_defe = {p.name: 1 if p.position == "Defender" and p.name in positives_names else 0 for p in players}
    negative_defe = {p.name: 1 if p.position == "Defender" and p.name in negatives_names else 0 for p in players}
    positive_mid = {p.name: 1 if p.position == "Midfield" and p.name in positives_names else 0 for p in players}
    negative_mid = {p.name: 1 if p.position == "Midfield" and p.name in negatives_names else 0 for p in players}
    positive_forw = {p.name: 1 if p.position == "Forward" and p.name in positives_names else 0 for p in players}
    negative_forw = {p.name: 1 if p.position == "Forward" and p.name in negatives_names else 0 for p in players}
    positive_ruk = {p.name: 1 if p.position == "Ruck" and p.name in positives_names else 0 for p in players}
    negative_ruk = {p.name: 1 if p.position == "Ruck" and p.name in negatives_names else 0 for p in players}


    myteam = {p.name: 1 if p.name in negatives_names else 0 for p in players}
    otherplayers = {p.name: 0 if p.name in negatives_names else 1 for p in players}



    prob = LpProblem("Fantasy Football",LpMaximize)
    player_vars = LpVariable.dicts("Players",player,0,1,LpBinary)
    prob += lpSum([value[i]*player_vars[i] for i in player]), "Total Points"
    prob += lpSum([price[i] * player_vars[i] for i in player]) <= budget, "Total Cost"

    prob += lpSum([positive_ruk[i] * player_vars[i] for i in player]) == ([negative_ruk[i] * player_vars[i] for i in player]), "Total Rucks"
    prob += lpSum([positive_defe[i] * player_vars[i] for i in player]) == ([negative_defe[i] * player_vars[i] for i in player]), "Total Defenders"

    ## FIXED NUMBER OF PLAYERS IN ONE POSITION COULD BE AERGUMETNS
    # prob += lpSum([positive_defe[i] * player_vars[i] for i in player]) == 1, "Total Defenders"

    # prob += lpSum([positive_mid[i] * player_vars[i] for i in player]) == 1, "Total Midfield"

    prob += lpSum([positive_mid[i] * player_vars[i] for i in player]) == ([negative_mid[i] * player_vars[i] for i in player]), "Total Midfield"
    prob += lpSum([positive_forw[i] * player_vars[i] for i in player]) == ([negative_forw[i] * player_vars[i] for i in player]), "Total Forward"

    prob += lpSum([myteam[i] * player_vars[i] for i in player]) == playersout, "Players Out"
    prob += lpSum([otherplayers[i] * player_vars[i] for i in player]) == playersin, "Players In"



    status = prob.solve()

    for key in player_vars:
        if player_vars[key].value() == 1:
            print(player_vars[key].__dict__)

    for p in players:
        if player_vars[p.name].value() == 1:
            print(p.__dict__)

    #    if(selected == 1):
    #        print(name)
    #return status

def runTradeOptimisation(myteam, budget, playersin, playersout, allplayersfile):
    positives = playersFromCSV(allplayersfile)
    names = [p.name for p in positives]

    negatives = []

    for name in myteam:
        index = isInListNameSubstitution(name, names)

        ## THE PLAYER DOES NOT HAVE AN ENTRY ##
        if index == -1: continue
        negatives.append(positives[index])
        del positives[index]
        del names[index]

    for p in negatives:
        p.price = -p.price
        p.value = -p.value

    print([p.name for p in negatives])

    all_players = positives + negatives
    linearOptimisationTrades(all_players, positives, negatives, budget, playersin, playersout)



def main():
#
    # players = playersFromCSV("players2021round2predictionsdup.csv")
#     #
#     for p in players:
#         if p.value == None or p.price == None or p.position not in ["Ruck", "Forward", "Midfield", "Defender"]:
#             players.remove(p)
#     linearOptimisation(players, False, 11604000)

    #######################################################
    ####################################################### NEEDS TO BE REFACTORED
    #######################################################

    myteam = ["Jake Lloyd", "Rory Laird", "Ben McEvoy", "Hunter Clark", "Hayden Young", "Alex Witherden", "Andrew Gaff", "Tim Taranto", "Rory Sloane", "Jye Caldwell", "Jackson Hately", "Tom Powell", "Errol Gulden", "Brodie Grundy", "Matt Flynn", "Paul Hunter", "Josh Dunkley", "Tom Phillips", "Jaidyn Stephenson", "James Rowe", "Nick Hind"]
    # runTradeOptimisation(myteam, 1145000, 2, 0, "players2021round2predictionsdup.csv")

    players = playersFromCSV("players2021round2predictionsdup.csv")
    runTradeOptimisation(myteam, 23000, 2, 2, "players2021round2predictionsdup.csv")



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
