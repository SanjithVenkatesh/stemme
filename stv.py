import operator, math

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