from abjad import *


def test_leaftools_iterate_leaf_pairs_forward_in_expr_01():

    score = Score([])
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'4")]
    score.append(Staff(notes))
    notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
    score.append(Staff(notes))
    contexttools.ClefMark('bass')(score[1])

    r'''
    \new Score <<
      \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'4
      }
      \new Staff {
            \clef "bass"
            c4
            a,4
            g,4
      }
    >>
    '''

    # make sure to show score if trying to verify test results     #
    # as the integer indices below are difficult to keep in mind. #

    pairs = leaftools.iterate_leaf_pairs_forward_in_expr(score)
    pairs = list(pairs)

    assert len(pairs) == 15
    assert pairs[0] == (score[0][0], score[1][0])
    assert pairs[1] == (score[0][0], score[0][1])
    assert pairs[2] == (score[1][0], score[0][1])
    assert pairs[3] == (score[0][1], score[0][2])
    assert pairs[4] == (score[0][1], score[1][1])
    assert pairs[5] == (score[1][0], score[0][2])
    assert pairs[6] == (score[1][0], score[1][1])
    assert pairs[7] == (score[0][2], score[1][1])
    assert pairs[8] == (score[0][2], score[0][3])
    assert pairs[9] == (score[1][1], score[0][3])
    assert pairs[10] == (score[0][3], score[0][4])
    assert pairs[11] == (score[0][3], score[1][2])
    assert pairs[12] == (score[1][1], score[0][4])
    assert pairs[13] == (score[1][1], score[1][2])
    assert pairs[14] == (score[0][4], score[1][2])
