#!/usr/bin/env python3


"""


Module Docstring
"""

__author__ = "Conor Wallwork"
__version__ = "0.1.0"
__license__ = "UWA"

from player import *
import numpy



from sys import stdin, stdout
import fileinput

from urllib.request import *
from bs4 import BeautifulSoup


class Page():

    ## get next page is an iterator function
    def __init__(self, url, getNextPage, isLastPage):
        self.url = url
        self.getNextPage = getNextPage
        self.isLastPage = isLastPage

    ## beautiful soup objects
    def getAllPages(self):
        page = urlopen(self.url).read()
        soup = BeautifulSoup(page)

        while(True):
            yield soup
            soup = self.getNextPage(soup)

            if(self.isLastPage(soup)):
                yield soup
                break


def partialseasonGetNextPage(soup):

    anchors = soup.find_all("a")
    for a in anchors:
        if a.get_text() == "❯":
            page = "https://www.footywire.com/afl/footy/"
            page += a["href"]
            page = urlopen(page).read()
            soup = BeautifulSoup(page)
            return soup
    return None

def partialseasonIsLastPage(soup):

    anchors = soup.find_all("a")
    for a in anchors:
        if a.get_text() == "❯":
            return False
    return True

def getPartialSeasonPlayerMatrix(players, firstRound, lastRound, url):
    page = Page(url, partialseasonGetNextPage, partialseasonIsLastPage)
    playerNames = [p.name for p in players]
    playermatrix = [[]]
    playermatrix[0] = playerNames
    playermatrix += [[0 for p in playerNames] for i in range(lastRound - firstRound + 1)]

    round = 1
    matrixrow = 1
    for p in page.getAllPages():
        if(round< firstRound):
            round += 1
            continue
        if(round > lastRound):
            break
        else:
            firstrow = p.find("td", {"class":"bnorm"}).parent
            for row in firstrow.find_next_siblings("tr"):
                name = row.contents[3]
                name = name.find("a").text
                points = row.contents[11]
                points = points.text

                found = False
                for i in range(len(playerNames)):
                    if playerNames[i] in name:
                        index = i
                        found = True
                        playermatrix[matrixrow][i] = points
                if not found: print(name)        
            #for name in playerNames:
            #    for row in round_table:
            #        print(row)
                    #if name == row.contents[1]:
                    #    print(row.contents[1])
            matrixrow += 1
        round += 1

    return playermatrix


def main():
    partialSeasonURL = "https://www.footywire.com/afl/footy/dream_team_round?year=2019&round=15&p=&s=T"
    page = Page(partialSeasonURL, partialseasonGetNextPage, partialseasonIsLastPage)

    players = getPlayersFromFile("players2019.csv", True)
    matrix = getPartialSeasonPlayerMatrix(players, 1, 23, "https://www.footywire.com/afl/footy/dream_team_round?year=2019&round=1&p=&s=T")

    a = numpy.asarray(matrix)
    numpy.savetxt("allrounds2019.csv", a, delimiter=",", fmt='%s')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
