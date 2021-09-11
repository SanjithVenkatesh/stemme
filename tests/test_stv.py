from methods.stv import stv


def test_stv():
    candidates = ["O", "P", "C", "S", "H"]
    vote_types = {"O": 4, "PO": 2, "CS": 8, "CH": 4, "S": 1, "H": 1}

    votes = generate_votes(vote_types)
    elected = stv(votes, 3, candidates)
    assert elected.sort() == ["C", "O", "S"].sort()


def generate_votes(vote_dict):
    all_votes = []
    for uv, votes in vote_dict.items():
        vote_list = []
        for char in uv:
            vote_list.append(char)
        for i in range(0, votes):
            all_votes.append(vote_list)

    return all_votes
