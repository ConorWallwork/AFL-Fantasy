# AFL-Fantasy
Utilities to scrape player data for AFL fantasy, predict future scores, and generate optimisations for a starting 22 under the $13M budget.
## Example Usage:
Clone the repo and run `python3 linear_optimisation.py`. This uses the file `players2021round2predictionsdup.csv` which was generated in Excel from round 1 scores. The result should be a list of 22 players which is the optimal team for round 2 of 2021 based on round 1 scores.

### player.py
Contains utilities to scrape player data from known sources once they are downloaded into an excel spreadsheet. Also contains utilities to store and retrieve player list to/from csv files.
### linear_optimisation.py
Contains utilities to find the optimal team under a given budget from a list of players. When each player has a position, price, and projected points, the optimisation can be done.
### partialseason.py
Contains utilities to generate averages between `firstRound` and `lastRound` for all players from a previous season.
### page.py
Contains an abstract data type `Page` which has the function `getAllPages` which allows one to implement the pagination for different websites.
### commentspage.py
Builds on `page.py` by defining a new type `CommentsPage` which inherits `Page` with additional functionality to list the comments from a page.
### tally.py
Contains utilities to tally player mentions from a comments list generated by `commentspage.py`.

