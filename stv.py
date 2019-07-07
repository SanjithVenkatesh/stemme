import operator, math

def stv(votes, seats, candidates): 
    # votes is a list of lists where each of the list is the order of preference for each voter, 
    # seats is an int representing the number of seats to fill
    # candidates is a list of all of the candidates standing for the election
    voteCount = size(votes)
    quota = math.floor(voteCount/seats) + 1
    candidateVoteCount = {x: 0 for x in candidates}
    seatsFilled = 0
    preferenceSpot = {x: 0 for x in votes}
    candidatesToReturn = list()
    while(seatsFilled < seats):
        for k,v in preferenceSpot.items():
            if(v < size(k)):
                candidateVoteCount[k[v]] += 1
                preferenceSpot[k] += 1
        for k,v in candidateVoteCount.items():
            anyonePromoted = False
            if v > quota:
                anyonePromoted = True
                candidatesToReturn.append(k)


        