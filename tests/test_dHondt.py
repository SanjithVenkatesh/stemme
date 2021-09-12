from os import name
from methods.dHondt import dHondt


def test_dHondt_with_dict():
    party_votes = {"A": 100, "B": 80, "C": 30, "D": 20}
    dh = dHondt(name="dh", seats=8, input=party_votes)
    party_seats = dh.calculate_winners()

    assert party_seats == {"A": 4, "B": 3, "C": 1, "D": 0}
