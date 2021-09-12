from methods.dHondt import dHondt
import pytest
from errors import InvalidCSVFileError

def test_dHondt_with_dict():
    party_votes = {"A": 100, "B": 80, "C": 30, "D": 20}
    dh = dHondt(name="dh", seats=8, input=party_votes)
    party_seats = dh.calculate_winners()

    assert party_seats == {"A": 4, "B": 3, "C": 1, "D": 0}

def test_dHondt_with_csv():
    party_votes = "party_votes.csv"
    dh = dHondt(name="dh", seats=8, input=party_votes)
    party_seats = dh.calculate_winners()

    assert party_seats == {"A": 4, "B": 3, "C": 1, "D": 0}


def test_throw_invalidcsvfileerror():
    party_votes = "invalid_party_vote.csv"

    with pytest.raises(InvalidCSVFileError):
        dh = dHondt(name="dh", seats=8, input=party_votes)

    