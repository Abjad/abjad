from abjad import *


def test_scoretools_add_double_bar_to_end_of_score_01():

    staff = Staff("c'4 d'4 e'4 f'4")
    scoretools.add_double_bar_to_end_of_score(staff)

    r'''
    \new Staff {
        c'4
        d'4
        e'4
        f'4
        \bar "|."
    }
    '''

    assert staff.format == '\\new Staff {\n\tc\'4\n\td\'4\n\te\'4\n\tf\'4\n\t\\bar "|."\n}'
