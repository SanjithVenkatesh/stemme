from typing import List

class Candidate:
    def __init__(self, name: str, party: str):
        self.name = name
        self.party = party

class Party:
    def __init__(self, names: list[str], party_name: str):
        self.party_members = names
        self.party_name = party_name
    
    def generate_candidates(self):
        candidates: List[Candidate] = []
        for member in self.party_members:
            candidates.append(Candidate(member, self.party_name))
        return candidates
    
    def generate_candidate(self, candidate_name):
        if candidate_name not in self.party_members:
            raise Exception("candidate not in party")
        return Candidate(candidate_name, self.party_name)

def mmp(votes, parties, seats, constituency_votes):
    winners = []

    return winners