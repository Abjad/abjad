from abjad import *


def test_scoretools_get_first_score_in_improper_parentage_of_component_01():


    staff = Staff("c'8 d'8 e'8 f'8")
    score = Score([staff])

    assert scoretools.get_first_score_in_improper_parentage_of_component(score.leaves[0]) is score
    assert scoretools.get_first_score_in_improper_parentage_of_component(score.leaves[1]) is score
    assert scoretools.get_first_score_in_improper_parentage_of_component(score.leaves[2]) is score
    assert scoretools.get_first_score_in_improper_parentage_of_component(score.leaves[3]) is score

    assert scoretools.get_first_score_in_improper_parentage_of_component(staff) is score
    assert scoretools.get_first_score_in_improper_parentage_of_component(score) is score
