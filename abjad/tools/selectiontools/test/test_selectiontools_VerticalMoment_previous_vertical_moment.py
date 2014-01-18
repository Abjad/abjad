# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_VerticalMoment_previous_vertical_moment_01():

    score = Score(r'''
        \new Staff {
            \times 4/3 {
                d''8
                c''8
                b'8
            }
        }
        \new PianoStaff <<
            \new Staff {
                a'4
                g'4
            }
        \new Staff {
            \clef "bass"
            f'8
            e'8
            d'8
            c'8
        }
        >>
        ''')

    last_leaf = score.select_leaves(allow_discontiguous_leaves=True)[-1]
    vertical_moment = inspect_(last_leaf).get_vertical_moment()
    assert vertical_moment.offset == Offset(3, 8)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(1, 3)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(1, 4)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(1, 6)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(1, 8)

    vertical_moment = vertical_moment.previous_vertical_moment
    assert vertical_moment.offset == Offset(0)
