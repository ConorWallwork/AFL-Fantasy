#!/usr/bin/env python3


"""


Module Docstring
"""

__author__ = "Conor Wallwork"
__version__ = "0.1.0"
__license__ = "UWA"


from sys import stdin, stdout
import fileinput

from urllib.request import *
from bs4 import BeautifulSoup



clubMap = {
"Power": "Port Adelaide Power",
"Giants": "Greater Western Sydney Giants",
"Crows": "Adeliade Crows",
"Eagles": "West Coast Eagles",
"Bulldogs": "Western Bulldogs",
"Demons": "Melbourne Demons",
"Swans": "Sydney Swans",
"Magpies": "Collingwood Magpies",
"Kangaroos": "North Melbourne Kangaroos",
"Tigers" : "Richmond Tigers",
"Blues": "Carlton Blues",
"Dockers": "Fremantle Dockers",
"Suns": "Gold Coast Suns",
"Saints": "St Kilda Saints",
"Hawks": "Hawthorn Hawks",
"Lions": "Brisbane Lions",
"Bombers": "Essendon Bombers",
"Cats": "Geelong Cats"
}

class Player():

    def __init__(self, name, value, price, position, club):
        self.name = name
        self.value = value
        self.price = price
        self.position = position
        self.club = club


    ##

def getPlayersFromFile(filename, hasPosition):
    nametok = 1
    clubtok = 2
    pricetok = 4
    pointstok = 7
    positiontok = 8
    players = []

    with fileinput.input(files=(filename)) as f:
        for line in f:
            vals = line.split(',')

            name = vals[nametok]
            club = clubMap[vals[clubtok]]
            price = int(vals[pricetok])
            points = float(vals[pointstok].strip())
            if(hasPosition):
                position = vals[positiontok].strip()
                p = Player(name, points, price, position, club)
            else:
                p = Player(name, points, price, "", club)

            players.append(p)
    return players



def main():
    """ Main entry point of the app """
    players = getPlayersFromFile("players2019.csv", True)
    for p in players:
        print(p.__dict__)

    #addPlayerPositionsToFile(players, "players2019.csv")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()



def getURLFromPlayer(player):

    base = "https://www.footywire.com/afl/footy/pp-"

    team = player.club.lower().replace(' ', '-')

    name = player.name.lower().replace(' ', '-')

    return base + team + "--" + name

def getPlayerPositionFromSite(p):
        url = getURLFromPlayer(p)

        page = urlopen(url).read()
        soup = BeautifulSoup(page)

        playerProfileData = soup.find_all(id="playerProfileData2")
        if(len(playerProfileData) == 0):
            position = "not found"
        else:
            position = playerProfileData[0].get_text().split()[-1]
        print(position)
        p.position = position
        return position

def addPlayerPositionsToFile(players, filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    i = 0
    for p in players:
        pos = getPlayerPositionFromSite(p)
        lines[i] = lines[i].strip()
        lines[i] += "," + pos + ","
        lines[i] += "\n"
        i += 1
    with open(filename, 'w') as file:
        file.writelines(data)
