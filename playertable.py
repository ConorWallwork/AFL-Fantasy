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




class PlayerTable:
    def __init__(self, tableFile, indexesMap, functionsMap):
        self.tableFile = tableFile
        self.indexesMap = indexesMap
        self.shortHandClubs = shortHandClubs
        self.shortHandPositions = shortHandPositions



    def tableToPlayers(self):
        with open(self.tableFile) as fp:
            print(fp)
            soup = BeautifulSoup(fp, 'html.parser')
            players = []

        # if(self.hasHeaders):
        #     headers = soup.find_all("tr")[0]
        #     for cell in headers.find_all("td"):
        #         self.headers.append(cell.text)
        for row in soup.find_all("tr"):
            player = Player("", "", "", "", "")
            cells = row.find_all("td")
            for key in self.indexesMap.keys():
                value = cells[self.indexesMap[key]].text
                if(key == "position" and self.shortHandPositions):
                    if("/" in value):
                        value = value.split("/")[0]
                    value = positionMap[value]
                if(key == "club" and self.shortHandClubs):
                    value = clubMap[value]
                setattr(player, key, value)
            players.append(player)
        return players




def main():
    indexesMap = {
                    "name":0,
                    "position":2,
                    "price": 7
    }
    pricestable = PlayerTable('html_tables/2021prices.html', indexesMap)
    players = pricestable.tableToPlayers()
    playersToCSV(players, "players2021prices.csv")

    playerprices = playersFromCSV("players2021prices.csv")

if __name__ == '__main__':
    main()
