from abjad import *


def test_iterationtools_iterate_staves_in_expr_01():

    score = Score(4 * Staff([]))
    score[0].name = '1'
    score[1].name = '2'
    score[2].name = '3'
    score[3].name = '4'

    for i, staff in enumerate(iterationtools.iterate_staves_in_expr(score, reverse=True)):
        assert staff.name == str(4 - i)


def test_iterationtools_iterate_staves_in_expr_02():

    score = Score(4 * Staff([]))
    score[0].name = '1'
    score[1].name = '2'
    score[2].name = '3'
    score[3].name = '4'

    for i, staff in enumerate(iterationtools.iterate_staves_in_expr(score)):
        assert staff.name == str(i + 1)
