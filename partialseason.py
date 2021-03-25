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
from player import *

from linear_optimisation import *

from urllib.request import *
from bs4 import BeautifulSoup


def getPartialSeasonPlayerMatrix(players, firstRound, lastRound, url):
    page = Page(url, partialseasonGetNextPage, partialseasonIsLastPage)
    playerNames = [p.name for p in players]
    playermatrix = [[]]
    playermatrix[0] = players
    playermatrix += [[0 for p in playerNames] for i in range(lastRound - firstRound + 1)]

    round = 1
    matrixrow = 1
    for p in page.getAllPages():
        if(round < firstRound):
            round += 1
            continue
        if(round > lastRound):
            break
        else:
            ## FIND THE FIRST ROW OF THE PLAYER TABLE
            firstrow = p.find("td", {"class":"bnorm"}).parent
            for row in firstrow.find_next_siblings("tr"):
                name = row.contents[3]
                name = name.find("a").text
                points = row.contents[11]
                points = points.text
                found = False
                index = -1
                for x in range(0, len(players)):
                    # if(name == "Brodie Grundy"):
                    #     #print(players[i].name)
                    if players[x].name in name:
                        index = x
                        found = True
                if not found:
                    firstName = name.split()[0]
                    possibleNames = getPossibleNames(firstName)
                    for pn in possibleNames:
                        names = name.split()
                        names[0] = pn
                        pn = " ".join(names)
                        for i in range(len(players)):
                            if players[i].name in pn:                                #print(pp.name)
                                index = i
                                found = True

                if found:
                    playermatrix[matrixrow][index] = points
                    if players[index].price == None or players[index].price == "":
                         price = row.contents[9].text

                         price = "".join([i for i in price if i.isnumeric()])
                         players[i].price = price
                if not found:
                    print(name+points)
                    findInPricesFile = getPlayerFromDTTALKFile("players2020DTTALK.csv", True, name)
                    if(findInPricesFile != None):
                        playermatrix[0].append(findInPricesFile)
                        for n in range(firstRound, lastRound+1):
                            playermatrix[n].append(0)
                        playermatrix[matrixrow][len(playermatrix[0]) - 1] = points
                        print(name+points)
            #for name in playerNames:
            #    for row in round_table:
            #        print(row)
                    #if name == row.contents[1]:
                    #    print(row.contents[1])
            matrixrow += 1
        round += 1
    return playermatrix

def playermatrixToCSV(matrix, filename):
    matrix[0] = [p.name for p in matrix[0]]
    a = numpy.asarray(matrix)
    numpy.savetxt(filename, a, delimiter=",", fmt='%s')

## RETURN PLAYER MATRIX WITH OBJECTS NOT NAMES
def playerMatrixFromCSV(filename):
    playermatrix = [[]]
    with open(filename, 'r', newline='')  as inputfile:
        i = 0
        for line in inputfile.readlines():
            if(i == 0):
                playernames = line.split(",")
                playermatrix[0] = playernames
            else:
                scores = line.split(",")
                scores = [int(i) for i in scores]
                playermatrix.append(scores)
            i += 1
    players = playersFromCSV("players2019.csv")
    for p in players:
        i = 0
        for playername in playermatrix[0]:
            if p.name == playername:
                playermatrix[0][i] = p
            i += 1

    return playermatrix

def getPartialAverages(players, firstRound, lastRound, minGames, matrixfile):
    playermatrix = playerMatrixFromCSV(matrixfile)

    for col in range(len(playermatrix[0])):
        games = [playermatrix[row][col] for row in range(firstRound, lastRound+1)]
        sum = 0
        played = 0
        for i in range(lastRound - firstRound + 1):
            sum += games[i]
            played += 1 if games[i] > 0 else 0
        if played > minGames:
            average = sum / float(played)
        else:
            average = sum / float(lastRound - firstRound + 1)
        players[col].value = average
        print(average)


def main():
    # partialSeasonURL = "https://www.footywire.com/afl/footy/dream_team_round?year=2019&round=15&p=&s=T"
    # page = Page(partialSeasonURL, partialseasonGetNextPage, partialseasonIsLastPage)
    #
    players = playersFromCSV("players2020.csv")
    # matrix = getPartialSeasonPlayerMatrix(players, 1, 18, "https://www.footywire.com/afl/footy/dream_team_round?year=2020&round=1&p=&s=T")
    # playersToCSV(players, "players2020.csv")

    # playermatrixToCSV(matrix, "allrounds2020.csv")
    #
    # matrix = playerMatrixFromCSV("allrounds2020.csv")
    # for p in players:
        # print(p.name)
    #
    getPartialAverages(players, 1, 3, 2, "allrounds2020.csv")
    playersToCSV(players, "players2020round3min2.csv")
    # playersToCSV(players, "players2019round5.csv")
    #
    # for p in players:
    #     if p.value == None or p.price == None or p.position not in ["Ruck", "Forward", "Midfield", "Defender"]:
    #         players.remove(p)
    #         print(p.name)
    #
    # linearOptimisation(players, False, 10000000)


    # for p in players[:4]:
    #     print(p.__dict__)



    # print(matrix)
    # a = numpy.asarray(matrix)
    # numpy.savetxt("firstround2019.csv", a, delimiter=",", fmt='%s')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
