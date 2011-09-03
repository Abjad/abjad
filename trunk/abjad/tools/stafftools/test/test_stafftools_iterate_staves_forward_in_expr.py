from abjad import *


def test_stafftools_iterate_staves_forward_in_expr_01():

    score = Score(4 * Staff([]))
    score[0].name = '1'
    score[1].name = '2'
    score[2].name = '3'
    score[3].name = '4'

    for i, staff in enumerate(stafftools.iterate_staves_forward_in_expr(score)):
        assert staff.name == str(i + 1)
