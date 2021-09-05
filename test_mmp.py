from mmp import mmp


def test_mmp():
    # Assembly foundations
    seats = 10
    # Registered Parties
    parties = ["SPD", "Union", "Grune", "Linke", "AFD"]

    # Party Vote
    party_vote = {"SPD": 250, "Union": 550, "Grune": 150, "Linke": 40, "AFD": 90}

    # Five constituencies
    berlin = {"SPD": 40, "Grune": 30, "Linke": 35, "Union": 20, "AFD": 5} # SPD winner
    saxony = {"SPD": 40, "Grune": 30, "Linke": 5, "Union": 50, "AFD": 90} # AFD winnder
    bavaria = {"SPD": 30, "Grune": 15, "Linke": 5, "Union": 100, "AFD": 20} # Union winner
    frankfurt = {"SPD": 25, "Grune": 45, "Linke": 15, "Union": 40, "AFD": 5} # Grune winner
    baden = {"SPD": 20, "Grune": 60, "Linke": 5, "Union": 40, "AFD": 15} # Grune winner

    # Party lists
    spd_list = create_list("spd", seats)
    union_list = create_list("u", seats)
    grune_list = create_list("g", seats)
    afd_list = create_list("afd", seats)
    linke_list = create_list("linke", seats)

    combined_party_lists = [spd_list, union_list, grune_list, afd_list, linke_list]
    constituency_votes = [berlin, saxony, bavaria, frankfurt, baden]

    candidates_elected = ["spd1", "spd2", "u1", "u2", "u3", "u4", "u5", "g1", "g2", "afd1"]

    assert mmp(party_vote, parties, 10, combined_party_lists, constituency_votes) == candidates_elected

def create_list(party_slug, seats):
    candidates = []
    for i in range(1,seats + 1):
        candidates.append(party_slug + str(i))
    return candidates