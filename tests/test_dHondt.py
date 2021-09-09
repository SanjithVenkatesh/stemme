from methods.dHondt import dHondt


def test_dHondt():
    party_votes = {"A": 100, "B": 80, "C": 30, "D": 20}
    party_seats = dHondt(8, party_votes)

    assert party_seats == {"A": 4, "B": 3, "C": 1, "D": 0}
