import operator

def mmp(votes, parties, constituencies, seats): 
    # votes is a list of dictionaries where keys are constituency, candidate, and party, 
    # parties are a list of parties in the entire nation, 
    # seats is the number of seats available in assembly
    # constituencies is the constituencies in the area
    partyVote = {x: 0 for x in parties}
    constituencyVote = {x: dict() for x in constituencies}
    for vote in votes:
        voteConst = votes["constituency"]
        if vote['party'] not in partyVote:
            partyVote[vote['party']] = 0
        partyVote[vote['party']] +=1 
        if vote['candidate'] not in constituencyVote[voteConst]:
            constituencyVote[voteConst][vote['candidate']] = 0
        constituencyVote[voteConst][vote['candidate']] += 1
    constWins = list()
    for const in constituencyVote:
        winningCandidate = max(const.items(), key=operator.itemgetter(1))[0]
        constWins.append(winningCandidate)
    seatsFilled = 0
    partySeats = dict()
    while seatsFilled < seats:
        continue
