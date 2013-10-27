# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_VerticalMoment___len___01():

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
    piano_staff = score[1]

    vertical_moment = inspect(score).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(Score<<2>>, Staff{1}, {@ 3:4 d''8, c''8, b'8 @}, d''8, PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"
    assert len(vertical_moment) == 9

    vertical_moment = inspect(score[0]).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(Staff{1}, {@ 3:4 d''8, c''8, b'8 @}, d''8)"
    assert len(vertical_moment) == 3

    vertical_moment = inspect(piano_staff).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"
    assert len(vertical_moment) == 5

    vertical_moment = inspect(piano_staff[0]).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(Staff{2}, a'4)"
    assert len(vertical_moment) == 2

    vertical_moment = inspect(piano_staff[1]).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(Staff{2}, e'8)"
    assert len(vertical_moment) == 2
