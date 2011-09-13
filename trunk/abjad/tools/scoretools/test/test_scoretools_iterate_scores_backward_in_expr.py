from abjad import *


def test_scoretools_iterate_scores_backward_in_expr_01():

    score_1 = Score([Staff("c'8 d'8 e'8 f'8")])
    score_2 = Score([Staff("c'1"), Staff("g'1")])
    scores = [score_1, score_2]

    scores = scoretools.iterate_scores_backward_in_expr(scores)
    scores = list(scores)

    assert scores[0] is score_2
    assert scores[1] is score_1
