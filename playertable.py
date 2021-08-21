from player import *
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

positionMap = { "RUC": "Ruck",
                "DEF": "Defender",
                "MID": "Midfield",
                "FWD": "Forward" }


## indexesMap contains the indexes of each attribute in the rows
## functionsMap contains the functions to generate values from the table data
## for example. A table may list positions as "RUC" but we want "Ruck"
class PlayerTable:
    def __init__(self, tableFile, indexesMap, functionsMap):
        self.tableFile = tableFile
        self.indexesMap = indexesMap
        self.functionsMap = functionsMap



    def tableToPlayers(self):
        with open(self.tableFile) as fp:
            print(fp)
            soup = BeautifulSoup(fp, 'html.parser')
            players = []

        for row in soup.find_all("tr"):
            player = Player("", "", "", "", "")
            cells = row.find_all("td")
            for key in self.indexesMap.keys():
                value = cells[self.indexesMap[key]].text
                value = self.functionsMap[key](value)
                setattr(player, key, value)
            players.append(player)
        return players

## choose the first position in "pos1/pos2" string
def DTTalkPositions(position):
    if("/" in position):
        position = position.split("/")[0]
    position = positionMap[position]
    return position

## EG ["Zac", "Zachary", "Zack", "Zach"] -> any of these goes to Zac
def standardiseName(name):
    names = name.split()
    possibleFirstNames = getPossibleNames(names[0])
    names[0] = possibleFirstNames[0]
    return " ".join(names)


def main():
    indexesMap = {
                    "name":1,
                    "club":2,
                    "value": 5
    }
    functionsMap = {
                    "name": standardiseName,
                    "club": lambda club: clubMap[club],
                    "value": lambda value: value ## the cell data does not need to be changed
    }
    pricestable = PlayerTable('html_tables/2021averages.html', indexesMap, functionsMap)
    players = pricestable.tableToPlayers()
    playersToCSV(players, "players2021averages.csv")


if __name__ == '__main__':
    main()
