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
    elected_candidates = list()
    preferential_votes = dict()
    round = 1
    totalCandidates = candidates
    for i in candidates:
        preferential_votes[i] = 0
    valid_votes = list()
    for vote in votes:
        if(len(vote) > 0):
            valid_votes.append(vote)
    votes = valid_votes
    quota = calculate_quota(len(votes), seats)
    print("quota is ", quota)

    while(len(elected_candidates) < seats):
        print()
        print("ROUND: ", round)
        print("elected candidates: ", elected_candidates)
        print("pref_votes: ", preferential_votes)
        print("Candidates in round: ", candidates)
        toRedistribute = list()
        roundCount = pref_count(votes)
        print("roundCount = ", roundCount)
        for candidate, votes in roundCount.items():
            if candidate in candidates:
                preferential_votes[candidate] += len(votes)
            print("Pref_count after counting pref_count function: ", preferential_votes)
            if(preferential_votes[candidate] >= quota):
                print("Candidate ", candidate, " has reached quota")
                elected_candidates.append((candidate, round))
                toRedistribute.append(candidate)
        if(len(toRedistribute) == 0):
            lowestCandidate = lowest_voted_candidate(preferential_votes)
            print("Candidate to be dropped: ", lowestCandidate)
            toRedistribute.append(lowestCandidate)
        if(len(elected_candidates) > seats):
            return countFinalPrefVote(elected_candidates, seats, preferential_votes)
        newVars = redistribute_votes(roundCount, toRedistribute, candidates)
        votes = turnVotesIntoLists(newVars[0])
        candidates = newVars[1]
        print("votes after redistribution: ", votes)
        round += 1
        print()
        

    return elected_candidates

def calculate_quota(validVotesCast, seatsToFill):
    return math.floor(validVotesCast/(seatsToFill + 1)) + 1

def calculate_transfer_votes(secondPrefVotes, originalVotes, surplusVotes):
    return math.floor((secondPrefVotes/originalVotes)*surplusVotes)

def countFinalPrefVote(elected, seats, pref_votes):
    print()
    print("IN countFinalPrefVote!")
    print(elected)
    firstTime = dict()
    for candRound in elected:
        if candRound[0] not in firstTime:
            firstTime[candRound[0]] = candRound[1]
    print(firstTime)
    sortedVote = sorted(firstTime.items(), key=lambda x: x[1])
    print(sortedVote)
    uniqueValues = set()
    selectedCandidates = list()
    selectedCandidatesRound = list()
    for candVote in sortedVote:
        uniqueValues.add(candVote[1])
        if(len(uniqueValues) <= seats):
            selectedCandidates.append(candVote[0])
            selectedCandidatesRound.append((candVote[0], candVote[1]))
    print("SCR: ",selectedCandidatesRound)
    if(len(selectedCandidates) == seats):
        print("SKIPPED FINAL FILTER!")
        return selectedCandidates
    highestRound = max(uniqueValues)
    goodCands = list()
    badCands = list()
    for cand in selectedCandidatesRound:
        print(cand)
        if(cand[1] == highestRound):
            badCands.append(cand[0])
        else:
            goodCands.append(cand[0])
    print("SCR after filter: ", goodCands)
    toCompare = dict()
    for cand in badCands:
        toCompare[cand] = pref_votes[cand]
    print("toCompare: ", toCompare)
    finalCand = max(toCompare.items(), key=operator.itemgetter(1))[0]
    goodCands.append(finalCand)
    print("SELECTED CANDIDATES: ", goodCands)
    return goodCands

# distributes the votes for each of their first preferential count
# in candidateCount, key is the candidate's name and the value is a list of the votes where the first value is the candidate's name
def pref_count(votes):
    candidateCount = dict()
    

    for vote in votes:
        print("candidateCount = ", candidateCount)
        print("vote in pref_count = ", vote)
        if len(vote) == 0:
            continue
        if vote[0] not in candidateCount:
            print("in vote not in candidate count: ", vote[0])
            candidateCount[vote[0]] = []
            candidateCount[vote[0]] = [vote]
        else:
            candidateCount[vote[0]].append(vote)

    return candidateCount

# given a dictionary where key is candidate and value being number of votes
# return the candidate with the least votes
def lowest_voted_candidate(pc):
    lowestCandidate = ""
    lowestVotes = float('inf')
    for candidate, votes in pc.items():
        if votes < lowestVotes:
            lowestCandidate = candidate
            lowestVotes = votes

    return lowestCandidate

#takes in the raw votes of each candidate and removes the first item before bundling them all back up together
def redistribute_votes(allVotes, toRedistribute, candidates):
    print("allVotes in redistribute: ", allVotes)
    print("toRedistribute in redistribute: ", toRedistribute)
    print("candidates in redistribute: ", candidates)
    totalVotes = list()
    newCandidates = list()
    for candidate, votes in allVotes.items():
        if candidate in toRedistribute:
            for vote in votes:
                totalVotes.append(vote.pop())
        else:
            for vote in votes:
                totalVotes.append(vote)
            newCandidates.append(candidate)

    return [totalVotes, newCandidates]

def turnVotesIntoLists(votes):
    listVotes = list()
    for vote in votes:
        if(isinstance(vote, str)):
            listVotes.append([vote])
        else:
            listVotes.append(vote)
    return listVotes


if __name__ == "__main__":
    print()
    votes = [["A", "B", "C"], ["B", "C"], ["B", "C", "A"], ["B"], ["A", "C"], ["C", "B", "A"], ["D", "B", "A"]]
    candidates = ["A", "B", "C", "D"]
    seats = 1
    print()
    print(stv(votes,seats, candidates))
