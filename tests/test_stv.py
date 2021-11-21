import pytest
from methods.stv import STV
from methods.base import Party, Candidate, create_list

seats = 3


@pytest.fixture
def A():
    return Party(names=create_list("a", seats), party_name="A", votes=100)


@pytest.fixture
def candA1(A: Party):
    return Candidate("A1", A)


@pytest.fixture
def candA2(A: Party):
    return Candidate("A2", A)


@pytest.fixture
def B():
    return Party(names=create_list("b", seats), party_name="B", votes=80)


@pytest.fixture
def candB1(B: Party):
    return Candidate("B1", B)


@pytest.fixture
def candB2(B: Party):
    return Candidate("B2", B)


@pytest.fixture
def C():
    return Party(names=create_list("c", seats), party_name="C", votes=30)


@pytest.fixture
def candC1(C: Party):
    return Candidate("C1", C)


@pytest.fixture
def candC2(C: Party):
    return Candidate("C2", C)


@pytest.fixture
def D():
    return Party(names=create_list("d", seats), party_name="D", votes=20)


@pytest.fixture
def candD1(D: Party):
    return Candidate("D1", D)


@pytest.fixture
def candD2(D: Party):
    return Candidate("D2", D)


@pytest.fixture
def E():
    return Party(names=create_list("e", seats), party_name="E", votes=20)


@pytest.fixture
def candE1(E: Party):
    return Candidate("E1", E)


@pytest.fixture
def candE2(E: Party):
    return Candidate("E2", E)


@pytest.fixture
def parties(A, B, C, D):
    return [A, B, C, D]


def test_stv(
    candA1,
    candB1,
    candC1,
    candD1,
    candE1,
    candA2,
    candB2,
    candC2,
    candD2,
    candE2,
    A,
    B,
    C,
    D,
    E,
):
    candidates1 = [candA1, candB1, candC1, candD1, candE1]
    candidates2 = [candA2, candB2, candC2, candD2, candE2]
    const1_vote_types = {
        (candA1): 4,
        (candB1, candA1): 2,
        (candC1, candD1): 8,
        (candC1, candE1): 4,
        (candD1): 1,
        (candE1): 1,
    }
    const2_vote_types = {
        (candA2): 4,
        (candC2, candB2): 1,
        (candA2, candE2): 6,
        (candD2, candA2): 9,
        (candD2): 2,
        (candE2): 3,
    }
    const1_votes = generate_votes(const1_vote_types)
    const2_votes = generate_votes(const2_vote_types)
    candidates = {"const1": candidates1, "const2": candidates2}
    votes = {"const1": const1_votes, "const2": const2_votes}
    seats = {"const1": 3, "const2": 3}

    stv = STV("test", votes, seats, candidates)
    elected = stv.constituency_winners("const1")

    stv.calculate_winners()

    assert elected.sort() == [candE1, candA1, candD1].sort()
    assert stv.party_seats == {C: 1, D: 2, A: 2, E: 1}
    assert stv.gallagher_index() == 5.7


def generate_votes(vote_dict):
    all_votes = []
    for vote_type, votes in vote_dict.items():
        if type(vote_type) is Candidate:
            vote_type = [vote_type]
        for _ in range(0, votes):
            all_votes.append(list(vote_type))

    return all_votes
