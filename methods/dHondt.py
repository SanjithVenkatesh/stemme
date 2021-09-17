import operator
import copy
from typing import Dict, List
import pandas as pd
from election import Election
from .base import Candidate, Party
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
    def add_vote(self, party: Party, votes: int):
        print(party, votes)
        if party in self.votes:
            raise PartyInElectionError
        self.votes[party] = votes

    # TODO: Have this work for a database import, ideally should be a different method
    # Returns a dictionary where the key is the party, value is the vote count
    def load_votes(self):
        if type(self.input) == list:
            self.load_votes_list()
        elif type(self.input) == str:
            self.load_votes_file()
        else:
            raise InvalidInputError
    
    # Read all information from the list of Party objects
    def load_votes_list(self):
        for party in self.input:
            try:
                self.add_vote(party, party.party_votes)
            except PartyInElectionError:
                pass

    # Read all of the votes from the Excel sheet
    # Ideally, the party is in the first column, the votes in the second column
    # Returns nothing, simply calls the add_vote function
    def load_votes_file(self):
        vote_df = pd.read_csv(self.input)
        
        columns = vote_df.columns
        if "Party" not in columns or "Votes" not in columns:
            raise InvalidCSVFileError
        
        # Create Party vote dictionary
        self.party_votes = pd.Series(vote_df.Votes.values,index=vote_df.Party).to_dict()
        
        # Get the party candidates
        column_headers: List[str] = vote_df
        for ch in column_headers:
            if ch not in ['Party', 'Votes']:
                candidate_names: List[str] = []
                for candidate in vote_df[ch].iteritems():
                    candidate_names.append(candidate)
                new_party: Party = Party(names=candidate_names, party_name=ch, votes=0)
                new_party.party_votes = self.party_votes[new_party.party_str()]
                try:
                    self.add_vote(new_party, new_party.party_votes)
                except PartyInElectionError:
                    # TODO: Implement logging system and add error message to queue
                    pass


    def calculate_winners(self, candidates=False, party_seats=False):
        # Do a deep copy of the votes into a new variable to track the weight of each party
        votesTemp = copy.deepcopy(self.votes)
        partySeats = {x: 0 for x in self.votes.keys()}
        candidates_elected = []

        # Loop through each seat and get which party gets that next seat
        # Calculate what the new weight of the party that won that seat
        for _ in range(0, self.seats):
            highestParty: Party = max(votesTemp.items(), key=operator.itemgetter(1))[0]
            there = highestParty in partySeats
            partySeats[highestParty] += 1
            candidates_elected.append(highestParty.pop_candidate())
            votesTemp[highestParty] = int(
                self.votes[highestParty] / (1 + partySeats[highestParty])
            )

        return candidates_elected if candidates and not party_seats else partySeats
