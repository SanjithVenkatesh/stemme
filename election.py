from abc import ABC, abstractmethod, abstractstaticmethod
from methods.base import Party, Poll
from typing import Dict, Tuple, List
from errors import InvalidKeyError


class Election(ABC):
    def __init__(self, name: str = ""):
        self.name = name
        self.polls: List[Poll] = []

    @abstractmethod
    def calculate_winners(self):
        pass

    @abstractmethod
    def add_vote(self):
        pass

    @abstractmethod
    def load_votes(self):
        pass

    # Method for transforming election results in order to calculate that election's Gallagher Index
    # The only true logic should be the creation of the party_stats dictionary
    # The implementation of the function should end up calling the calculate_gallagher_index static method
    @abstractmethod
    def gallagher_index(self):
        pass

    # Method for predicting the election based on the polls given as well as previous elections
    # @abstractmethod
    # def predict_winners(self):
    #     pass

    # Calculate the Gallagher index for the election
    # party_stats is a Dictionary where key is a Party, and value is a tuple where first value is num seats and second value is num votes
    @staticmethod
    def calculate_gallagher_index(party_stats: Dict[Party, Tuple[int, int]]):
        # Calculate total seats and votes
        total_seats: int = 0
        total_votes: int = 0

        for stats in party_stats.values():
            total_seats += stats[0]
            total_votes += stats[1]

        # Calculate the difference in percentages between the vote and seat share for each party
        party_difference_squared: Dict[Party, float] = {}
        for party, stats in party_stats.items():
            try:
                vote_share = stats[1] / total_votes
                seats_share = stats[0] / total_seats
            except Exception:
                raise InvalidKeyError
            diff2 = ((vote_share - seats_share) * 100) ** 2
            party_difference_squared[party] = diff2

        total_diff_squared = sum(party_difference_squared.values())
        return round((total_diff_squared / 2) ** 0.5, 2)

    def get_metadata(self):
        return f"Election {self.name} has {str(len(self.votes))}"

    def __str__(self):
        return self.get_metadata()

    def __repr__(self):
        return self.get_metadata()
