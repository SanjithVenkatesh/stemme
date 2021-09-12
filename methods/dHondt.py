import operator
import copy
import pandas as pd
from election import Election
from errors import PartyInElectionError, InvalidCSVFileError, InvalidInputError

class dHondt(Election):
    
    # Init function for creating dHondt object
    # Unique args is the seats arg to get how many seats available in assembly, Excel file where the votes are
    # Input can be either a direct dict object or a CSV file that contains the values
    def __init__(self, name: str, seats: int, input):
        super().__init__(name)
        self.votes = dict()
        self.input = input
        self.seats = seats
        self.load_votes()

    # Arg is a new party with their party vote
    def add_vote(self, party: str, votes: int):
        if party in self.votes:
            raise PartyInElectionError
        self.votes[party] = votes
    
    
    # TODO: Have this work for a database import, ideally should be a different method
    # Returns a dictionary where the key is the party, value is the vote count
    def load_votes(self):
        if type(self.input) == dict:
            self.votes = self.input
        elif type(self.input) == str:
            self.load_votes_file()
        else:
            raise InvalidInputError


    # Read all of the votes from the Excel sheet
    # Ideally, the party is in the first column, the votes in the second column
    # Returns nothing, simply calls the add_vote function
    def load_votes_file(self):
        vote_df = pd.read_csv(self.input)
        columns = vote_df.columns
        if "Party" not in columns or "Votes" not in columns:
            raise InvalidCSVFileError
        for _, row in vote_df.iterrows():
            try:
                self.add_vote(row['Party'], row['Votes'])
            except PartyInElectionError:
                # TODO: Implement logging system and add error message to queue
                pass

    
    def calculate_winners(self):
        # Do a deep copy of the votes into a new variable to track the weight of each party
        votesTemp = copy.deepcopy(self.votes)
        parties = self.votes.keys()
        partySeats = {x: 0 for x in parties}

        # Loop through each seat and get which party gets that next seat
        # Calculate what the new weight of the party that won that seat
        for i in range(0, self.seats):
            highestParty = max(votesTemp.items(), key=operator.itemgetter(1))[0]
            partySeats[highestParty] += 1
            votesTemp[highestParty] = int(
                self.votes[highestParty] / (1 + partySeats[highestParty])
            )

        return partySeats
