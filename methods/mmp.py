from typing import List, Dict, Tuple
from errors import InvalidConstituencyError, InvalidInputError
from .base import Party, Candidate
import math
from election import Election
import matplotlib.pyplot as plt


class MMP(Election):
    def __init__(
        self,
        name: str,
        party_vote: Dict[Party, int],
        parties: List[str],
        seats: int,
        constituency_votes: Dict[str, Dict[Candidate, int]],
    ):
        super().__init__(name=name)
        self.votes = party_vote
        self.parties = parties
        self.seats = seats
        self.constituency_votes: Dict[str, Dict[Candidate, int]] = constituency_votes
        self.party_seats = {x: 0 for x in self.parties}

    def add_vote(self, party_vote: Party, const_vote: Candidate, constituency):
        if constituency not in self.constituency_votes.keys():
            self.constituency_votes[constituency] = {const_vote: 0}
        if party_vote not in self.votes:
            self.votes[party_vote] = 0
        self.constituency_votes[constituency][const_vote] += 1
        self.votes[party_vote] += 1

    def load_votes(self):
        pass

    # Calculate the Gallager Index for the election
    # Transform the election results and call upon the Election.calculate_gallagher_index function
    def gallagher_index(self):
        party_stats = {party: (0, 0) for party in self.parties}
        for party, party_vote in self.votes:
            party_stats[party][1] = party_vote
        for party, party_seats in self.votes:
            party_stats[party][0] = party_seats

        return Election.calculate_gallagher_index(party_stats)

    def calculate_winners(self):
        winners: List[str] = []

        # Initialize blank dict for seats awarded for each party
        seats_awarded: Dict[Party, int] = {x: 0 for x in self.parties}

        # Quota needed to gain a seat based on party vote
        quota = self.sum_values(self.votes) / self.seats

        # Calculate guarenteed seats before taking remainder into account, create remainder dict for each party
        remainder = {x: 0 for x in self.parties}
        for party, votes in self.votes.items():
            seats_awarded[party] += math.floor(votes / quota)
            remainder[party] = (votes / quota) - seats_awarded[party]

        seats_awarded_so_far = self.sum_values(seats_awarded)
        remaining_seats = self.seats - seats_awarded_so_far
        highest_remainders: List[Party] = sorted(remainder, key=remainder.get, reverse=True)[
            :remaining_seats
        ]

        for party in highest_remainders:
            seats_awarded[party] += 1

        # Determine elected candidates, see what parties they are a part of
        con_party_winners: Dict[Party, int] = {x: 0 for x in self.parties}
        for const_vote in self.constituency_votes.values():
            winner: Candidate = self.constituency_winner(const_vote)
            winners.append(winner)
            self.party_seats[winner.party] += 1
            winner.party.remove_candidate(winner)
            con_party_winners[winner.party] += 1

        # Get the rest of the winners by going through each party list
        for party in self.parties:
            remaining_winners: int = seats_awarded[party] - con_party_winners[party]
            for i in range(0, remaining_winners):
                winners.append(party.generate_candidate_by_rank(i))
                self.party_seats[party] += 1

        return winners.sort()

    def sum_values(self, d: dict):
        only_values = d.values()
        return sum(only_values)

    def constituency_winner(self, con: Dict[Candidate, int]) -> str:
        winner = sorted(con, key=con.get, reverse=True)[:1]
        return winner[0]
    
    # Plot out the results of the chart
    def plot_seats_results(self, emphasis: Party = None):
        party_names = []
        emphasis_vals = []
        party_colors = []
        for party in self.party_seats.keys():
            party_names.append(party.to_str())
            emphasis_vals.append(0.1 if party == emphasis else 0)
            party_colors.append(party.party_color)

        seats = self.party_seats.values()

        fig1, ax1 = plt.subplots()
        ax1.pie(seats, labels=party_names, autopct='%1.1f%%', startangle=90, explode=emphasis_vals, colors=party_colors)
        ax1.axis('equal')
        plt.title("Pie Chart of Seats Won by Party")

        plt.show()

