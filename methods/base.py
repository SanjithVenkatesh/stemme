from typing import List, Dict, Optional


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
    def __init__(self, names: Optional[List[str]], party_name: str, votes: int):
        self.party_members = names
        self.party_name = party_name
        self.party_votes = votes

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


def create_list(party_slug, seats):
    candidates = []
    for i in range(1, seats + 1):
        candidates.append(party_slug + str(i))
    return candidates
