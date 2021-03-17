#!/usr/bin/env python3


"""


Module Docstring
"""

__author__ = "Conor Wallwork"
__version__ = "0.1.0"
__license__ = "UWA"


from sys import stdin, stdout
from page import *
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

positionMap = { "RUC": "Ruck",
                "DEF": "Defender",
                "MID": "Midfield",
                "FWD": "Forward" }

def getPossibleNames(firstName):
    namesubstitutions = [["Josh", "Joshua"], ["Nicholas", "Nick", "Nic"], ["Mitch", "Mitchell"], ["Tim", "Timothy"], ["Jonathan", "John", "Jon", "Jonathon"],
                        ["Oliver", "Ollie"], ["Dan", "Daniel"], ["Zac", "Zachary", "Zack", "Zach"], ["Thomas", "Tom"]]
    for subs in namesubstitutions:
        if firstName in subs:
            return subs
    return []

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
def getPlayersFromDTTALKFile(filename, usesFirstLastFormat):
    nametok = 0
    postok = 1
    pricetok = 4
    players = []
    with fileinput.input(files=(filename)) as f:
        for line in f:
            vals = line.split(',')
            price = int(vals[pricetok])
            name = vals[nametok]
            if usesFirstLastFormat:
                name = name ## do nothing
            else:
                name = name.split()
                name = name[-1] +   " "+ " ".join(name[0:-1])
            position = vals[postok]
            if '/' in position: position = position.split('/')[0]
            position = positionMap[position]

            players.append(Player(name, None, price, position, None))

    return players

def getPlayerFromDTTALKFile(filename, usesFirstLastFormat, playerName):
    with fileinput.input(files=(filename)) as f:
        nametok = 0
        postok = 1
        pricetok = 4
        player = None
        with fileinput.input(files=(filename)) as f:
            for line in f:
                vals = line.split(',')
                price = int(vals[pricetok])
                name = vals[nametok]
                if(name != playerName):
                    continue
                if usesFirstLastFormat:
                    name = name ## do nothing
                else:
                    name = name.split()
                    name = name[-1] +   " "+ " ".join(name[0:-1])
                position = vals[postok]
                if '/' in position: position = position.split('/')[0]
                position = positionMap[position]
                player = Player(name, None, price, position, None)
                return player
        return None

def getPlayersFromPricesFile(filename, hasPosition):
    nametok = 1
    clubtok = 2
    pricetok = 4
    # pointstok = 7
    positiontok = 8
    players = []

    with fileinput.input(files=(filename)) as f:
        for line in f:
            vals = line.split(',')

            name = vals[nametok]
            club = clubMap[vals[clubtok]]
            price = int(vals[pricetok])
            # points = float(vals[pointstok].strip())
            if(hasPosition):
                position = vals[positiontok].strip()
                p = Player(name, None, price, position, club)
            else:
                p = Player(name, None, price, "", club)

            players.append(p)
    return players

def getPlayersFromAveragesFile(filename):
    players = []
    with fileinput.input(files=(filename)) as f:
         i = 0
         for line in f:
             vals = line.split(",")
             name = vals[1]
             club = clubMap[vals[2]]
             value = vals[4].strip()
             players.append(Player(name, value, None, None, club))

    return players

def getPlayerPricesFromHardCode():
    prices = {
    "Josh P. Kennedy": 654000,
    "Sydney Stack": 170000
    }
    return prices
############################################################
############################################################
############################################################
############################################################



## ENCODE AND DECODE OUR PLAYER OBJECTS ##
############################################################
############################################################
############################################################
def playersToCSV(players, filename):
    import csv
    toCSV = [player.__dict__ for player in players]
    keys = toCSV[0].keys()
    with open(filename, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writerows(toCSV)

def playersFromCSV(filename):
    nametok = 0
    valuetok = 1
    pricetok = 2
    positiontok = 3
    clubtok = 4
    players = []
    with open(filename, 'r', newline='')  as inputfile:
        for line in inputfile:
            vals = line.split(",")
            name = vals[nametok] if vals[nametok] != "" else None
            club = vals[clubtok].strip() if vals[clubtok] != "" else None
            value = float(vals[valuetok]) if vals[valuetok] != "" else None
            price = int(vals[pricetok]) if vals[pricetok] != "" else None
            position = vals[positiontok] if vals[positiontok] != "" else None
            players.append(Player(name, value, price, position, club))
    return players
############################################################
############################################################
############################################################
############################################################


## GET PLAYER DATA FOR A YEAR ###
def getAllPlayers(player_averages_file, DTTALK_prices_file, usesFirstLastFormat, player_prices_file):
    players_prices = getPlayersFromDTTALKFile(DTTALK_prices_file, usesFirstLastFormat)
    players_averages = getPlayersFromAveragesFile(player_averages_file)

    ## ADD THE PRICES FROM DTTALK FILE TO THE AVERAGES FILE
    for pp in players_prices:
        found = False
        for pa in players_averages:
            if pp.name.lower() == pa.name.lower():
                pa.price = pp.price
                pa.position = pp.position
                found = True

    ## TRY THE OTHER LIST OF PRICES FROM FOOTY WIRE
    players_pricesOLD = getPlayersFromPricesFile(player_prices_file, False)
    for pp in players_pricesOLD:
        found = False
        for pa in players_averages:
            if pp.name.lower() == pa.name.lower():
                pa.price = pp.price
                found = True

    ## FIND NAMES WITH COMMON SUBSITUTES
    # hardCodedPrices = getPlayerPricesFromHardCode()
    for pa in players_averages:
        if pa.price == None:
            firstName = pa.name.split()[0]
            possibleNames = getPossibleNames(firstName)
            for pn in possibleNames:
                names = pa.name.split()
                names[0] = pn
                name = " ".join(names)
                print(name)
                for pp in players_prices:
                    if pp.name == name:
                        #print(pp.name)
                        pa.price = pp.price
                        pa.position = pp.position
            # if pa.name in hardCodedPrices.keys():
            #     pa.price = hardCodedPrices[pa.name]

        ## SEE IF THEIR PRICE IS ENTERED AT A LATER ROUND
        # getPartialSeasonPlayerMatrix(players_averages, 1, 3, "https://www.footywire.com/afl/footy/dream_team_round?year=2019&round=1&p=&s=T")

    for pa in players_averages:
        if pa.position == None:
            getPlayerPositionFromSite(pa)
    return players_averages


def main():
    """ Main entry point of the app """
    #
    players = getAllPlayers("players2020averages.csv", "players2020DTTALK.csv", True, "players2020prices.csv")
    playersToCSV(players, "players2020.csv")
    #
    # playerdicts = []
    # for p in players:
    #     playerdicts.append(p.__dict__)
    #
    # playersToCSV(playerdicts, "newplayers2019.csv")
    #

    #addPlayerPositionsToFile(players, "players2019.csv")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
