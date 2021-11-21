import math
import random
from typing import Dict, List
from .base import Candidate, Party
from errors import InvalidConstituencyError

from election import Election


class STV(Election):
    def __init__(
        self,
        name: str,
        votes: Dict[str, List[List[Candidate]]],
        seats: Dict[str, int],
        candidates: Dict[str, List[Candidate]],
        debug=False,
    ):
        super().__init__(name=name)
        self.votes = votes
        self.seats = seats
        self.candidates = candidates
        self.debug = debug
        self.party_seats: Dict[Party, int] = dict()

    # Calculates the winners in all constituencies
    # Does not return anything, sets values in self.party_seats
    def calculate_winners(self):
        # Loop through the votes dictionary and retrieve the candidates list for constituency
        # Run the constituency_winner function to get the winners
        # Get the party for each winner and add it to party_seats
        for const_name, const_votes in self.votes.items():
            const_candidates = self.candidates[const_name]
            const_seats = self.seats[const_name]
            const_winners: List[Candidate] = self.__constituency_winner(
                const_votes, const_seats, const_candidates
            )

            for winner in const_winners:
                if winner.party not in self.party_seats:
                    self.party_seats[winner.party] = 1
                else:
                    self.party_seats[winner.party] += 1

    # Calculates the winner of a given constituency
    # Checks if the votes exist for particular constituency, throws exception if votes do not exist
    def constituency_winners(self, constituency: str) -> List[Candidate]:
        if (
            constituency not in self.votes
            or constituency not in self.candidates
            or constituency not in self.seats
        ):
            raise InvalidConstituencyError
        const_votes = self.votes[constituency]
        const_candidates = self.candidates[constituency]
        const_seats = self.seats[constituency]

        return self.__constituency_winner(const_votes, const_seats, const_candidates)

    def __constituency_winner(
        self, votes, seats, candidates, debug=False
    ) -> List[Candidate]:
        # votes is a list of lists where each of the list is the order of preference for each voter,
        # seats is an int representing the number of seats to fill
        # candidates is a list of all of the candidates standing for the election
        # first need is to calculate the quota which each candidate will need to get with their preferential count
        # quota = floor(valid votes cast/seats to fill + 1) + 1
        # in the first count, each vote's first choice is counted and distributed to each candidate
        # we will keep this in a preferential count dictionary
        # if any candidate reaches the quota then they are declared elected
        # the surplus of each elected candidate's vote is then distributed among next preference votes
        # this will be done by removing the first item in the list and counting up the next preference of all of those
        # formula for surplus: (votes for next preference belonging to the original candidate/total votes for original candidate)* surplus votes for original candidate
        # for example, if candidate got 12 votes and quota is 6, then there are 6 surplus votes
        # if 8 of the 12 people had candidate B as their second choice, then candidate B will get (8/12)*6 = 4 extra votes
        # continue redistributing votes until all seats are filled
        elected_candidates: List[Candidate] = list()
        preferential_votes: Dict[Candidate, int] = dict()
        round: int = 1
        for i in candidates:
            preferential_votes[i] = 0
        valid_votes: List[List[str]] = list()
        for vote in votes:
            if len(vote) > 0:
                valid_votes.append(vote)
        votes: List[List[str]] = valid_votes
        quota = self.calculate_quota(len(votes), seats)
        if debug:
            print("quota is ", quota)

        while len(elected_candidates) < seats:
            if debug:
                print()
                print("ROUND: ", round)
                print("elected candidates: ", elected_candidates)
                print("pref_votes: ", preferential_votes)
                print("Candidates in round: ", candidates)
            toRedistribute = list()
            roundCount = self.pref_count(votes)
            if debug:
                print("roundCount = ", roundCount)
            for candidate, votes in roundCount.items():
                if candidate in candidates:
                    preferential_votes[candidate] += len(votes)
                if debug:
                    print(
                        "Pref_count after counting pref_count function: ",
                        preferential_votes,
                    )
                if preferential_votes[candidate] >= quota:
                    if debug:
                        print("Candidate ", candidate, " has reached quota")
                    elected_candidates.append((candidate, round))
                    toRedistribute.append(candidate)
            if len(toRedistribute) == 0:
                lowestCandidate = self.lowest_voted_candidate(preferential_votes)
                if debug:
                    print("Candidate to be dropped: ", lowestCandidate)
                toRedistribute.append(lowestCandidate)
            if len(elected_candidates) > seats:
                return self.countFinalPrefVote(
                    elected_candidates, seats, preferential_votes, debug=debug
                )
            newVars = self.redistribute_votes(roundCount, toRedistribute, candidates)
            votes = self.turnVotesIntoLists(newVars[0])
            candidates = newVars[1]
            if debug:
                print("votes after redistribution: ", votes)
            round += 1

        return elected_candidates

    def calculate_quota(self, validVotesCast, seatsToFill):
        return math.floor(validVotesCast / (seatsToFill + 1)) + 1

    def calculate_transfer_votes(self, secondPrefVotes, originalVotes, surplusVotes):
        return math.floor((secondPrefVotes / originalVotes) * surplusVotes)

    # Add a new vote to the constituency
    # Need to verify that the constituency already exists
    def add_vote(self, vote: List[Candidate], constituency: str):
        if constituency not in self.votes.keys():
            raise InvalidConstituencyError
        self.votes[constituency].append(vote)

    def load_votes(self):
        pass

    def countFinalPrefVote(self, elected, seats, pref_votes, debug):
        if debug:
            print()
            print("In countFinalPrefVote!")
            print(elected)
        firstTime = dict()
        for candRound in elected:
            if candRound[0] not in firstTime:
                firstTime[candRound[0]] = candRound[1]
        if debug:
            print(firstTime)
        sortedVote = sorted(firstTime.items(), key=lambda x: x[1])
        if debug:
            print(sortedVote)
        uniqueValues = set()
        selectedCandidates = list()
        selectedCandidatesRound = list()
        for candVote in sortedVote:
            uniqueValues.add(candVote[1])
            if len(uniqueValues) <= seats:
                selectedCandidates.append(candVote[0])
                selectedCandidatesRound.append((candVote[0], candVote[1]))
        if debug:
            print("SCR: ", selectedCandidatesRound)
        if len(selectedCandidates) == seats:
            return selectedCandidates
        highestRound = max(uniqueValues)
        goodCands = list()
        badCands = list()
        for cand in selectedCandidatesRound:
            if cand[1] == highestRound:
                badCands.append(cand[0])
            else:
                goodCands.append(cand[0])
        if debug:
            print("SCR after filter: ", goodCands)
        toCompare = dict()
        for cand in badCands:
            toCompare[cand] = pref_votes[cand]
        finalCand = ""
        if self.allValuesSame(toCompare):
            finalCand = random.choice(list(toCompare.keys()))
            goodCands.append(finalCand)
        else:
            sortedKeys = sorted(toCompare, key=lambda key: toCompare[key])
            sortedKeys.reverse()
            for i in range(0, seats - len(goodCands)):
                goodCands.append(sortedKeys[i])
        return goodCands

    def allValuesSame(self, d):
        uniqueValues = set()
        for k, v in d.items():
            uniqueValues.add(v)
            if len(uniqueValues) == 2:
                return False
        return True

    # distributes the votes for each of their first preferential count
    # in candidateCount, key is the candidate's name and the value is a list of the votes where the first value is the candidate's name
    def pref_count(self, votes):
        candidateCount = dict()

        for vote in votes:
            if len(vote) == 0:
                continue
            if vote[0] not in candidateCount:
                candidateCount[vote[0]] = []
                candidateCount[vote[0]] = [vote]
            else:
                candidateCount[vote[0]].append(vote)

        return candidateCount

    # given a dictionary where key is candidate and value being number of votes
    # return the candidate with the least votes
    def lowest_voted_candidate(self, pc):
        lowestCandidate = ""
        lowestVotes = float("inf")
        for candidate, votes in pc.items():
            if votes < lowestVotes:
                lowestCandidate = candidate
                lowestVotes = votes

        return lowestCandidate

    # takes in the raw votes of each candidate and removes the first item before bundling them all back up together
    def redistribute_votes(self, allVotes, toRedistribute, candidates):
        totalVotes = list()
        newCandidates = list()
        for candidate, votes in allVotes.items():
            if candidate in toRedistribute:
                type_of_vote_count = {}
                for vote in votes:
                    tu_vote = tuple(vote)
                    if tu_vote not in type_of_vote_count:
                        type_of_vote_count[tu_vote] = 1
                    else:
                        type_of_vote_count[tu_vote] += 1
                type_of_vote_count_trim = {}
                for vote, count in type_of_vote_count.items():
                    vote = list(vote)
                    vote.pop(0)
                    vote = tuple(vote)
                    type_of_vote_count_trim[vote] = count
                for vote, count in type_of_vote_count_trim.items():
                    for _ in range(0, count):
                        totalVotes.append(list(vote))
            else:
                for vote in votes:
                    totalVotes.append(vote)
                newCandidates.append(candidate)

        return [totalVotes, newCandidates]

    def turnVotesIntoLists(self, votes):
        listVotes = list()
        for vote in votes:
            if isinstance(vote, str):
                listVotes.append([vote])
            else:
                listVotes.append(vote)
        return listVotes

    def unique_votes(self, votes):
        tup = []
        for vote in votes:
            vote = tuple(vote)
            tup.append(vote)
        lst = list(set(tup))
        unq = []
        for l in lst:
            unq.append(list(l))
        print(unq)
        return unq

    def gallagher_index(self):
        party_votes: Dict[Party, int] = dict()
        for const_votes in self.votes.values():
            for vote_list in const_votes:
                for vote in vote_list:
                    if vote.party not in party_votes:
                        party_votes[vote.party] = 1
                    else:
                        party_votes[vote.party] += 1
        party_stats = dict()
        for party in party_votes.keys():
            if party not in self.party_seats:
                self.party_seats[party] = 0
            party_stats[party] = (self.party_seats[party], party_votes[party])

        return Election.calculate_gallagher_index(party_stats)
