import operator
import copy


def dHondt(
    seats, votes
):  # seats is an integer representing number of seats available, votes is a dictionary with key being party, value being number of votes received

    # Do a deep copy of the votes into a new variable to track the weight of each party
    votesTemp = copy.deepcopy(votes)
    parties = votes.keys()
    partySeats = {x: 0 for x in parties}

    # Loop through each seat and get which party gets that next seat
    # Calculate what the new weight of the party that won that seat
    for i in range(0, seats):
        highestParty = max(votesTemp.items(), key=operator.itemgetter(1))[0]
        partySeats[highestParty] += 1
        votesTemp[highestParty] = int(
            votes[highestParty] / (1 + partySeats[highestParty])
        )
        
    return partySeats
