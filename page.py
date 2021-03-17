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


class Page():

    ## get next page is an iterator function
    def __init__(self, url, getNextPage, isLastPage):
        self.url = url
        self.getNextPage = getNextPage
        self.isLastPage = isLastPage

    ## beautiful soup objects
    def getAllPages():
        page = urlopen(url).read()
        soup = BeautifulSoup(page)

        yield soup
        while(!self.isLastPage(soup)):
            soup = self.getNextPage(soup)
            yield soup




def partialRoundGetNextPage(soup):

    anchors = soup.find_all("a")
    for a in anchors:
        if a.get_text() == "❯":
            page = urlopen(a["href"]).read()
            soup = BeautifulSoup(page)
            return soup
    return None

def partialRoundIsLastPage(soup):
    
