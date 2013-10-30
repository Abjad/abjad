# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_VerticalMoment___eq___01():

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

    vertical_moment_1 = inspect(piano_staff).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

    vertical_moment_2 = inspect(piano_staff).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

    assert vertical_moment_1 == vertical_moment_2
    assert not vertical_moment_1 != vertical_moment_2


def test_selectiontools_VerticalMoment___eq___02():

    score = Score([])
    score.append(Staff([scoretools.FixedDurationTuplet(
        Duration(4, 8), "d''8 c''8 b'8")]))
    piano_staff = scoretools.PianoStaff(r'''
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
        ''')
    score.append(piano_staff)

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
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
        >>
        '''
        )

    vertical_moment_1 = inspect(
        piano_staff).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

    vertical_moment_2 = inspect(
        piano_staff[0]).get_vertical_moment_at(Offset(1, 8))
    "VerticalMoment(Staff{2}, a'4, Staff{4}, e'8)"

    assert not vertical_moment_1 == vertical_moment_2
    assert vertical_moment_1 != vertical_moment_2
