from player import *
from sys import stdin, stdout
import fileinput

from urllib.request import *
from bs4 import BeautifulSoup


class PlayerTable:
    def __init__(self, tableFile, indexesMap):
        self.tableFile = tableFile
        self.indexesMap = indexesMap



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
                setattr(player, key, cells[self.indexesMap[key]].text)
            print(player.__dict__)




def main():
    indexesMap = {
                    "name":1,
                    "club":2,
                    "value": 5
    }
    footywiretable = PlayerTable('html_tables/footywire2021averages.html', indexesMap)
    footywiretable.tableToPlayers()


if __name__ == '__main__':
    main()
