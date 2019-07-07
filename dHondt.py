import operator

def dHondt(seats,votes): #seats is an integer representing number of seats available, votes is a dictionary with key being party, value being number of votes received
    votesTemp = votes
    print(votesTemp)
    parties = votes.keys()
    partySeats = {x:0 for x in parties}
    for i in range(0,seats):
        highestParty = max(votesTemp.items(), key=operator.itemgetter(1))[0]
        print(highestParty)
        partySeats[highestParty] += 1
        votesTemp[highestParty] = votesTemp[highestParty]/(1+partySeats[highestParty])
    return partySeats


if __name__ == '__main__':
    votes = {'Brexit': 5248533-271404-233006, 'Labour': 2347255-127833-146724, 'LibDem': 3367284-113885-218285, 'Conservative': 1512809-54587-182476, 'Green': 1881306-52660, 'UKIP': 554463-27566-28418, 'ChangeUK': 551846-24332-30004}
    seats = 63
    print(dHondt(seats, votes))

    