from typing import List, Dict, Optional

from numpy import datetime64, double


class Candidate:
    def __init__(self, name: str, party):
        self.name: str = name
        self.party: Party = party

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name


class Party:
    def __init__(
        self, names: Optional[List[Candidate]], party_name: str, votes: int, color: str
    ):
        self.party_members = names
        self.party_name = party_name
        self.party_votes = votes
        self.party_color = color

    def generate_candidates(self) -> List[Candidate]:
        candidates: List[Candidate] = []
        for member in self.party_members:
            candidates.append(Candidate(member, self))
        self.party_members = candidates
        return candidates

    def generate_candidate(self, candidate_name) -> Candidate:
        if candidate_name not in self.party_members:
            raise Exception("candidate not in party")
        return Candidate(candidate_name, self.party_name)

    def remove_candidate(self, c: Candidate) -> None:
        self.party_members.remove(c)

    def pop_candidate(self):
        return self.party_members.pop(0)

    def generate_candidate_by_rank(self, rank: int):
        if rank < len(self.party_members):
            return self.party_members[rank]
        else:
            return None

    def party_str(self) -> str:
        return self.party_name

    def __str__(self) -> str:
        return self.party_str()

    def __repr__(self) -> str:
        return self.party_str()

    def __hash__(self):
        return hash((self.party_name, self.party_votes))

    def __eq__(self, other):
        return (self.party_name, self.party_votes) == (
            other.party_name,
            other.party_votes,
        )

    def to_str(self):
        return self.party_str()

class Pollster:
    def __init__(self, name: str):
        self.name = name
        self.polls: List[Poll] = []
    
    def __repr__(self):
        return self.to_str()
    
    def __str__(self):
        return self.to_str()
    
    def to_str(self):
        return self.name

class Poll:
    def __init__(self, pollster: Pollster, stats: Dict[Party, double], date: datetime64):
        self.pollster: Pollster = pollster
        self.stats: Dict[Party, double] = stats
        self.date: datetime64 = date
    
    def __repr__(self):
        return self.to_str()
    
    def __str__(self):
        return self.to_str()

    def to_str(self):
        to_print: str = "{"
        for party, percentage in self.stats.items():
            to_print += party + " : " + str(percentage) + ","
        to_print = to_print[:-1] + "}"
        return to_print


def create_list(party_slug, seats):
    candidates = []
    for i in range(1, seats + 1):
        candidates.append(party_slug + str(i))
    return candidates
