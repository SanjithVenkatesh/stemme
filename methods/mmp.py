from typing import List, Dict
from .base import Party, Candidate
import math
from election import Election


class MMP(Election):
    def __init__(
        self,
        name: str,
        party_vote: Dict[Party, int],
        parties: List[str],
        seats: int,
        constituency_votes,
    ):
        super().__init__(name=name)
        self.votes = party_vote
        self.parties = parties
        self.seats = seats
        self.constituency_votes = constituency_votes

    def add_vote(self):
        pass

    def load_votes(self):
        self.votes = self.party_vote

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
        highest_remainders = sorted(remainder, key=remainder.get, reverse=True)[
            :remaining_seats
        ]

        for party in highest_remainders:
            seats_awarded[party] += 1

        # Determine elected candidates, see what parties they are a part of
        con_party_winners: Dict[Party, int] = {x: 0 for x in self.parties}
        for const_vote in self.constituency_votes:
            winner: Candidate = self.constituency_winner(const_vote)
            winners.append(winner.name)
            winner.party.remove_candidate(winner)
            con_party_winners[winner.party] += 1

        # Get the rest of the winners by going through each party list
        for party in self.parties:
            remaining_winners: int = seats_awarded[party] - con_party_winners[party]
            for i in range(0, remaining_winners):
                winners.append(party.generate_candidate_by_rank(i))

        return winners.sort()

    def sum_values(self, d: dict):
        only_values = d.values()
        return sum(only_values)

    def constituency_winner(self, con: Dict[Candidate, int]) -> str:
        winner = sorted(con, key=con.get, reverse=True)[:1]
        return winner[0]
