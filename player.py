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
"Cats": "Geelong Cats",
"Collingwood": "Collingwood Magpies",
"Western Bulldogs": "Western Bulldogs",
"West Coast": "West Coast Eagles",
"GWS": "Greater Western Sydney Giants",
"Melbourne": "Melbourne Demons",
"Adelaide": "Adeliade Crows",
"Essendon": "Essendon Bombers",
"Sydney": "Sydney Swans",
"Geelong": "Geelong Cats",
"Port Adelaide": "Port Adelaide Power",
"Fremantle": "Fremantle Dockers",
"Gold Coast": "Gold Coast Suns",
"Brisbane": "Brisbane Lions",
"Richmond": "Richmond Tigers",
"Carlton": "Carlton Blues",
"Hawthorn": "Hawthorn Hawks",
"St Kilda": "St Kilda Saints",
"North Melbourne": "North Melbourne Kangaroos"
}

class Player():

    def __init__(self, name, value, price, position, club):
        self.name = name
        self.value = value
        self.price = price
        self.position = position
        self.club = club


## DEPRECATED POSITION METHOD ##
############################################################
############################################################
############################################################
def getURLFromPlayer(player):

    base = "https://www.footywire.com/afl/footy/pp-"

    team = player.club.lower().replace(' ', '-')

    name = player.name.lower().replace(' ', '-')

    return base + team + "--" + name


    ##
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


############################################################
############################################################
############################################################
############################################################


### GET PLAYER DATA FROM RAW FILES ###
############################################################
############################################################
############################################################
def getPlayersFromDTTALKFile(filename):
    nametok = 0
    pricetok = 4
    players = []
    with fileinput.input(files=(filename)) as f:
        for line in f:
            vals = line.split(',')
            name = vals[nametok]
            price = int(vals[pricetok])

            name = name.split()
            name = name[-1] +   " "+ " ".join(name[0:-1])
            players.append(Player(name, None, price, None, None))

    return players

def getPlayersFromPricesFile(filename, hasPosition):
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
############################################################
############################################################
############################################################
############################################################

def playersToCSV(players):
    import csv
    toCSV = players
    keys = toCSV[0].keys()
    with open('players2019.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)



def main():
    """ Main entry point of the app """
    players_prices = getPlayersFromDTTALKFile("players2019DTTALK.csv")

    for pp in players_prices:
        print(pp.__dict__)
    players_averages = []
    with fileinput.input(files=("players2019averages.csv")) as f:
         i = 0
         for line in f:
             vals = line.split(",")
             name = vals[1]
             club = clubMap[vals[2]]
             value = vals[4].strip()
             players_averages.append(Player(name, value, None, None, club))
    for pp in players_prices:
        found = False
        for pa in players_averages:
            if pp.name.lower() == pa.name.lower():
                pa.price = pp.price
                found = True

    players_pricesOLD = getPlayersFromPricesFile("OLDplayers2019.csv", True)
    for pp in players_pricesOLD:
        found = False
        for pa in players_averages:
            if pp.name.lower() == pa.name.lower():
                print(pp.name)
                pa.price = pp.price
                found = True
    ##for pa in players_averages:
    ##    position = getPlayerPositionFromSite(pa)
    ##    pa.position = position

    for pa in players_averages:
        #print(pa.__dict__)
        continue

    players_averages = [pa.__dict__ for pa in players_averages]
    playersToCSV(players_averages)

    #addPlayerPositionsToFile(players, "players2019.csv")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
