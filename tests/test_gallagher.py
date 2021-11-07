from election import Election
from methods.base import Party, create_list
import pytest

seats = 8

@pytest.fixture
def Liberal():
    return Party(names=create_list('l', seats), party_name='Liberal', votes=100)

@pytest.fixture
def Conservative():
    return Party(names=create_list('c', seats), party_name='Conservative', votes=80)

@pytest.fixture
def NDP():
    return Party(names=create_list('n', seats), party_name='NDP', votes=30)

@pytest.fixture
def BQ():
    return Party(names=create_list('bq', seats), party_name='BQ', votes=20)

@pytest.fixture
def Greens():
    return Party(names=create_list('g', seats), party_name='Greens', votes=20)

@pytest.fixture
def Other():
    return Party(names=create_list('o', seats), party_name='Other', votes=20)

def test_calculate_gallager_index(Liberal, Conservative, NDP, BQ, Greens, Other):
    party_stats = {Liberal: (184, 3947), Conservative: (99, 3189), NDP: (44, 1971), BQ: (10, 466), Greens: (1, 345), Other: (0, 82)}

    assert Election.calculate_gallagher_index(party_stats=party_stats) == 12.02
