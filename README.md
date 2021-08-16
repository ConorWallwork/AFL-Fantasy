# AFL-Fantasy
### player.py
Contains utilities to scrape player data from known sources once they are downloaded into an excel spreadsheet. Also contains utilities to store and retrieve player list to/from csv files.
### partialseason.py
Contains utilities to generate averages between `firstRound` and `lastRound` for all players from a previous season.
### page.py
Contains an abstract data type `Page` which has the function `getAllPages` which allows one to implement the pagination for different websites.
### commentspage.py
Builds on `page.py` by defining a new type `CommentsPage` which inherits `Page` with additional functionality to generate the comments from this page.
### tally.py


