from methods.dHondt import dHondt
import pytest
from errors import InvalidCSVFileError
from methods.base import Party, create_list

seats = 8

@pytest.fixture
def A():
    return Party(names=create_list('a', seats), party_name='A', votes=100)

@pytest.fixture
def B():
    return Party(names=create_list('b', seats), party_name='B', votes=80)

@pytest.fixture
def C():
    return Party(names=create_list('c', seats), party_name='C', votes=30)

@pytest.fixture
def D():
    return Party(names=create_list('d', seats), party_name='D', votes=20)

@pytest.fixture
def parties(A, B, C, D):
    return [A,B,C,D]


def test_dHondt_with_list_candidates(parties):
    dh = dHondt(name="dh", seats=8, input=parties)
    print("dh votes: " , dh.votes)
    winning_candidates = dh.calculate_winners(candidates=True)
    print(winning_candidates)

    assert winning_candidates == ['a1', 'b1', 'a2', 'b2', 'a3', 'c1', 'b3', 'a4']

def test_dHondt_with_dict_party_seats(parties, A, B, C, D):
    dh = dHondt(name="dh", seats=8, input=parties)
    winning_candidates = dh.calculate_winners(party_seats=True)

    assert winning_candidates == {A: 4, B: 3, C: 1, D: 0}

def test_dHondt_with_csv(A, B, C, D):
    party_votes = "dHondt_csv/party_votes.csv"
    dh = dHondt(name="dh", seats=8, input=party_votes)
    party_seats = dh.calculate_winners()

    assert party_seats == {A: 4, B: 3, C: 1, D: 0}


def test_throw_invalidcsvfileerror():
    party_votes = "dHondt_csv/invalid_party_votes.csv"

    with pytest.raises(InvalidCSVFileError):
        dh = dHondt(name="dh", seats=8, input=party_votes)

    