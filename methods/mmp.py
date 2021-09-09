from typing import List, Dict
import math


class Candidate:
    def __init__(self, name: str, party):
        self.name: str = name
        self.party: Party = party

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Party:
    def __init__(self, names: list[str], party_name: str):
        self.party_members = names
        self.party_name = party_name

    def generate_candidates(self) -> List[Candidate]:
        candidates: List[Candidate] = []
        for member in self.party_members:
            candidates.append(Candidate(member, self))
        return candidates

    def generate_candidate(self, candidate_name) -> Candidate:
        if candidate_name not in self.party_members:
            raise Exception("candidate not in party")
        return Candidate(candidate_name, self.party_name)

    def remove_candidate(self, c: Candidate) -> None:
        self.party_members.remove(c.name)

    def generate_candidate_by_rank(self, rank: int):
        if rank < len(self.party_members):
            return self.party_members[rank]
        else:
            return None


def mmp(
    party_vote: Dict[Party, int], parties: List[str], seats: int, constituency_votes
):
    winners: List[str] = []

    # Initialize blank dict for seats awarded for each party
    seats_awarded: Dict[Party, int] = {x: 0 for x in parties}

    # Quota needed to gain a seat based on party vote
    quota = sum_values(party_vote) / seats

    # Calculate guarenteed seats before taking remainder into account, create remainder dict for each party
    remainder = {x: 0 for x in parties}
    for party, votes in party_vote.items():
        seats_awarded[party] += math.floor(votes / quota)
        remainder[party] = (votes / quota) - seats_awarded[party]

    seats_awarded_so_far = sum_values(seats_awarded)
    remaining_seats = seats - seats_awarded_so_far
    highest_remainders = sorted(remainder, key=remainder.get, reverse=True)[
        :remaining_seats
    ]

    for party in highest_remainders:
        seats_awarded[party] += 1

    # Determine elected candidates, see what parties they are a part of
    con_party_winners: Dict[Party, int] = {x: 0 for x in parties}
    for const_vote in constituency_votes:
        winner: Candidate = constituency_winner(const_vote)
        winners.append(winner.name)
        winner.party.remove_candidate(winner)
        con_party_winners[winner.party] += 1

    # Get the rest of the winners by going through each party list
    for party in parties:
        remaining_winners: int = seats_awarded[party] - con_party_winners[party]
        for i in range(0, remaining_winners):
            winners.append(party.generate_candidate_by_rank(i))

    return winners.sort()


def sum_values(d):
    only_values = d.values()
    return sum(only_values)


def constituency_winner(con: Dict[Candidate, int]) -> str:
    winner = sorted(con, key=con.get, reverse=True)[:1]
    return winner[0]
