from mmp import mmp, Candidate, Party


def test_mmp():
    # Assembly foundations
    seats = 10

    # Party lists
    spd_list = create_list("spd", seats)
    union_list = create_list("u", seats)
    grune_list = create_list("g", seats)
    afd_list = create_list("afd", seats)
    linke_list = create_list("linke", seats)
    print(spd_list)

    SPD = Party(spd_list, "SPD")
    Grune = Party(grune_list, "Grune")
    Union = Party(union_list, "Union")
    AFD = Party(afd_list, "AFD")
    Linke = Party(linke_list, "Linke")

    # Party Vote
    party_vote = {SPD: 250, Union: 550, Grune: 150, Linke: 40, AFD: 90}

    # Registered Parties
    parties = [SPD, Grune, Union, AFD, Linke]

    # Candidate Lists
    spd_candidates = SPD.generate_candidates()
    union_candidates = Union.generate_candidates()
    grune_candidates = Grune.generate_candidates()
    afd_candidates = AFD.generate_candidates()
    linke_candidates = Linke.generate_candidates()
    print(spd_candidates)

    # Five constituencies
    berlin = { spd_candidates[0]: 40, grune_candidates[0]: 30, linke_candidates[0]: 35, union_candidates[0]: 20, afd_candidates[0]: 5} # SPD winner
    saxony = {spd_candidates[1]: 40, grune_candidates[1]: 30, linke_candidates[1]: 5, union_candidates[1]: 50, afd_candidates[1]: 90} # AFD winnder
    bavaria = {spd_candidates[2]: 30, grune_candidates[2]: 15, linke_candidates[2]: 5, union_candidates[2]: 100, afd_candidates[2]: 20} # Union winner
    frankfurt = {spd_candidates[3]: 25, grune_candidates[3]: 45, linke_candidates[3]: 15, union_candidates[3]: 40, afd_candidates[3]: 5} # Grune winner
    baden = {spd_candidates[4]: 20, grune_candidates[4]: 60, linke_candidates[4]: 5, union_candidates[4]: 40, afd_candidates[4]: 15} # Grune winner

    constituency_votes = [berlin, saxony, bavaria, frankfurt, baden]

    candidates_elected = ["spd1", "spd2", "u1", "u2", "u3", "u4", "u5", "g1", "g2", "afd1"]

    mmp_winners = mmp(party_vote, parties, 10, constituency_votes)

    assert mmp_winners == candidates_elected

def create_list(party_slug, seats):
    candidates = []
    for i in range(1,seats + 1):
        candidates.append(party_slug + str(i))
    return candidates