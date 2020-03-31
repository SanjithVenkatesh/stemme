import operator, math
import sys

def stv(votes, seats, candidates): 
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
    elected_candidates = set()
    preferential_votes = dict()
    for i in candidates:
        preferential_votes[i] = 0

    quota = calculate_quota(len(votes), seats)

    while(len(elected_candidates) != seats):
        toRedistribute = set()
        roundCount = pref_count(votes)
        for candidate, votes in roundCount.items():
            preferential_votes[candidate] += len(votes)
            if(preferential_votes[candidate] >= quota):
                elected_candidates.add(candidate)
                toRedistribute.add(candidate)
        if(len(toRedistribute) == 0):
            lowestCandidate = lowest_voted_candidate(pref_count)
            toRedistribute.add(lowestCandidate)
        votes = redistribute_votes(roundCount, toRedistribute)
        

    return elected_candidates

def calculate_quota(validVotesCast, seatsToFill):
    return math.floor(validVotesCast/(seatsToFill + 1)) + 1

def calculate_transfer_votes(secondPrefVotes, originalVotes, surplusVotes):
    return math.floor((secondPrefVotes/originalVotes)*surplusVotes)

# distributes the votes for each of their first preferential count
# in candidateCount, key is the candidate's name and the value is a list of the votes where the first value is the candidate's name
def pref_count(votes):
    candidateCount = dict()

    for vote in votes:
        if len(vote) == 0:
            continue
        if vote[0] not in candidateCount:
            candidateCount[vote[0]] = (vote)
        else:
            candidateCount[vote[0]].append(vote)

    return candidateCount

# given a dictionary where key is candidate and value being number of votes
# return the candidate with the least votes
def lowest_voted_candidate(prefCount):
    lowestCandidate = ""
    lowestVotes = float('inf')
    for candidate, votes in prefCount.items():
        if votes < lowestVotes:
            lowestCandidate = candidate
            lowestVotes = votes

    return lowestCandidate

#takes in the raw votes of each candidate and removes the first item before bundling them all back up together
def redistribute_votes(allVotes, toRedistribute):
    totalVotes = list()
    for candidate, votes in allVotes.items():
        if candidate in toRedistribute:
            for vote in votes:
                totalVotes.append(vote.pop())
        else:
            for vote in votes:
                totalVotes.append(vote)

    return totalVotes
