from abc import abstractmethod


from abc import ABC, abstractmethod

class Election(ABC):
    def __init__(self, name: str = ""):
        self.name = name
    
    @abstractmethod
    def calculate_winners(self):
        pass
    
    @abstractmethod
    def add_vote(self):
        pass

    @abstractmethod
    def load_votes(self):
        pass
    
    def get_metadata(self):
        return f"Election {self.name} has {str(len(self.votes))}"
    
    def __str__(self):
        return self.get_metadata()
    
    def __repr__(self):
        return self.get_metadata()
