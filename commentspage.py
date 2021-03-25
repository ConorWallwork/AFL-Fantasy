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



from sys import stdin, stdout
import fileinput

from urllib.request import *
from bs4 import BeautifulSoup


class CommentsPage(Page):

    # def getAllParentComments(self):
    #     comments = []
    #     self.getFirstCommentFunction(self)
    #     while(not self.isLastCommentFunction(self)):
    #         comments.append(self.comment)
    #         self.comment = self.getNextCommentFunction(self)
    #     comments.append(self.comment)
    #     return comments

    def CommentsPage(self, soup):
        self.soup = soup

    def getAllComments(self):
        return self.soup.find_all("div", "comment-inner")

def getRawComments(commentList):
    comments = []
    for c in commentList:
        text = c.find("div", "c")
        text = text.get_text()
        comments += text.split()
    return comments


    # def addComment(self, comment):
    #     self.comment = comment
    #
    # def addGetNextCommentFunction(self, getNextCommentFunction):
    #     self.getNextCommentFunction = getNextCommentFunction
    #
    # def addisLastCommentFunction(self, isLastCommentFunction):
    #     self.isLastCommentFunction = isLastCommentFunction
    #
    # def addGetFirstCommentFunction(self, getFirstCommentFunction):
    #     self.getFirstCommentFunction = getFirstCommentFunction

# def getFirstCommentDTTALK(commentPage):
#
#     first = commentPage.soup.find("div", "comment-inner")
#     commentPage.addComment(first)
#     return first
#
# def getNextCommentDTTALK(commentsPage):
#     next = None
#
#     parent = commentsPage.comment.find_parent("li", "comment")
#     if(parent.find_next_sibling("li", "comment") != None):
#         next = parent.find_next_sibling("li", "comment").find("div", "comment-inner")
#
#     return next
#
# def isLastCommentDTTALK(commentsPage):
#     return getNextCommentDTTALK(commentsPage) == None

def DTTALKcommentsPageFactory(url):
    commentsPage = CommentsPage(url, None, DTTALKcommentsGetNextPage, DTTALKcommentsIsLastPage)
    # commentsPage.addGetNextCommentFunction(getNextCommentDTTALK)
    # commentsPage.addisLastCommentFunction(isLastCommentDTTALK)
    # commentsPage.addGetFirstCommentFunction(getFirstCommentDTTALK)
    return commentsPage

def getAllCommentAllPages(DTTALKurl):
    comments = []
    commentspage = DTTALKcommentsPageFactory(DTTALKurl)
    for p in commentspage.getAllPages():
        nextpage = CommentsPage("", p, DTTALKcommentsGetNextPage, DTTALKcommentsIsLastPage)
        thiscomments = nextpage.getAllComments()
        comments += thiscomments
    return comments


def main():


    commentspage = DTTALKcommentsPageFactory("https://dreamteamtalk.com/2020/03/12/my-team-2020-version-3-0/comment-page-3/#comments")

    comments = getAllCommentAllPages("https://dreamteamtalk.com/2020/02/06/my-team-2020-version-1-2/")
    comments = getRawComments(comments)

    f = open("comments2020myteam1.2", 'w', encoding='utf8')
    f.write(' '.join(comments))
    # print(comments2020.getRawComments(comments))
    # partialSeasonURL = "https://www.footywire.com/afl/footy/dream_team_round?year=2019&round=15&p=&s=T"
    # page = Page(partialSeasonURL, partialseasonGetNextPage, partialseasonIsLastPage)
    #
    # players = playersFromCSV("players2019.csv")
    # matrix = getPartialSeasonPlayerMatrix(players, 1, 1, "https://www.footywire.com/afl/footy/dream_team_round?year=2019&round=1&p=&s=T")
    #
    # print(matrix)
    # a = numpy.asarray(matrix)
    # numpy.savetxt("firstround2019.csv", a, delimiter=",", fmt='%s')
    #

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
