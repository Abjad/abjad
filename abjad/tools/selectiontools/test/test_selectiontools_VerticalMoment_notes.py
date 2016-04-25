# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_VerticalMoment_notes_01():

    score = Score(
        r'''
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
        '''
        )

    staff_group = score[1]

    vertical_moment = inspect_(score).get_vertical_moment_at(Offset(1, 8))

    "(Note(d'', 8), Note(a', 4), Note(e', 8))"

    assert vertical_moment.notes == (
        score[0][0][0], staff_group[0][0], staff_group[1][1])
