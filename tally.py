#!/usr/bin/env python3


"""


Module Docstring
"""

__author__ = "Conor Wallwork"
__version__ = "0.1.0"
__license__ = "UWA"

from player import *
import numpy
from page import *
from commentspage import *

import numpy as np
from scipy import stats
import numpy as np



from sys import stdin, stdout
import fileinput

from urllib.request import *
from bs4 import BeautifulSoup

## Returns a list of the indexes of the players mentioned in the word
## Naive approach to tallying where shared last names result in all players being tallied
def getPlayerIndexesNaive(playernames, comments, commentIndex):
    ## Map player pseudonyms onto real last name
    lastName = makeNameSubstitutions(comments[commentIndex])

    return [i for i in range(len(playernames)) if playernames[i].split()[-1].lower() == lastName.lower()]

## Given a word, check if it is a pseudonym and if so return the actual last name
## Otherwise return word
def makeNameSubstitutions(word):
    pseudonymsMap = {
    "Dusty": "Martin",
    "Cogs": "Coniglio",
    "Danger": "Dangerfield",
    "Bont": "Bontempelli"
    }

    if word in pseudonymsMap.keys():
        return pseudonymsMap[word]
    else:
        return word

## Return a list of tallies for each player by index
def getPlayerMentionsTallies(players, comments):
    tallies = [0]*len(players)

    names = [p.name for p in players]
    indexes = None
    for i in range(len(comments)):
        indexes = getPlayerIndexesNaive(names, comments, i)
        for ind in indexes:
            tallies[ind] += 1
    ## if len(indexes) > 1:
    ## index = resolveName(player, comments, index) ??


    return tallies

def dictionariesToCSV(dicts, outputfile):
    import csv
    toCSV = dicts
    keys = toCSV[0].keys()
    with open(outputfile, 'w', newline='')  as of:
        dict_writer = csv.DictWriter(of, keys)
        dict_writer.writerows(toCSV)

def linearRegression(xvals, yvals):
    x = np.array(xvals)
    y = np.array(yvals)
    return stats.linregress(x, y)

def main():
    """ Main entry point of the app """


    myteam = ["Jake Lloyd", "Rory Laird", "Ben McEvoy", "Hunter Clark", "Hayden Young", "Alex Witherden", "Jacob Koschitzke", "Thomas Highmore", "Andrew Gaff", "Tim Taranto", "Rory Sloane", "Matt Rowell", "Jye Caldwell", "Jackson Hately", "Tom Powell", "Errol Gulden", "Tyler Brockman", "James Jordon", "Brodie Grundy", "Matt Flynn", "Paul Hunter", "Josh Dunkley", "Tom Phillips", "Jaidyn Stephenson", "Braeden Campbell", "James Rowe", "Nick Hind", "Harrison Jones", "Chad Warner", "Lloyd Meek"]

    players = getPlayersFromPricesFile("2021round2.csv")

    negatives = [p for p in players if p.name in myteam]
    # # comments = getAllCommentAllPages("https://dreamteamtalk.com/2020/03/12/my-team-2020-version-3-0/")
    # # comments = getRawComments(comments)
    #
    # f = open("comments2020myteamMARCH", 'r', encoding='utf-8')
    # comments = f.read().split()
    #
    # players = playersFromCSV("players2020round5.csv")
    #
    # tallies = getPlayerMentionsTallies(players, comments)
    #
    # ppds = getPlayerPointsPerDollar(players)
    #
    #
    # playersdicts = [p.__dict__ for p in players]
    # for i in range(len(players)):
    #     playersdicts[i]["mentions"] = tallies[i]
    #     playersdicts[i]["points per dollar"] = ppds[i]
    #
    # # playersdicts = [p for p in playersdicts if p["price"] != None]
    # # playersdicts = [p for p in playersdicts if int( p["price"] ) < 400000]
    # # playersdicts = [p for p in playersdicts if int( p["mentions"]) > 3]
    #
    # dictionariesToCSV(playersdicts, "players2020_round5_mentionsMARCH.csv")
    #
    # print(linearRegression([p["mentions"] for p in playersdicts], [p["points per dollar"] for p in playersdicts]))

    #
    # players2019 = playersFromCSV("players2019.csv")
    # players2020 = playersFromCSV("players2020.csv")
    #
    # ppd2019 = getPlayerPointsPerDollar(players2019)
    # ppd2020 = getPlayerPointsPerDollar(players2020)
    #
    # ppd19shared = []
    # ppd20shared = []
    #
    # for i in range(len(players2019)):
    #     for j in range(len(players2020)):
    #         if players2019[i].name == players2020[j].name:
    #             ppd19shared.append(ppd2019[i])
    #             ppd20shared.append(ppd2020[j])
    #
    # print(linearRegression(ppd19shared, ppd20shared))




if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
