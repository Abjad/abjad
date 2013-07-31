# -*- encoding: utf-8 -*-
from abjad import *


def test_Score_add_double_bar_01():

    staff = Staff("c'4 d'4 e'4 f'4")
    score = Score([staff])
    score.add_double_bar()

    r'''
    \new Score <<
        \new Staff {
            c'4
            d'4
            e'4
            f'4
            \bar "|."
        }
    >>
    '''

    assert score.lilypond_format == '\\new Score <<\n\t\\new Staff {\n\t\tc\'4\n\t\td\'4\n\t\te\'4\n\t\tf\'4\n\t\t\\bar "|."\n\t}\n>>'
