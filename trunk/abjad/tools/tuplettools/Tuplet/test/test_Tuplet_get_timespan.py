# -*- encoding: utf-8 -*-
from abjad import *


def test_Tuplet_get_timespan_01():

    staff = Staff(r"c'4 d'4 \times 2/3 { e'4 f'4 g'4 }")
    score = Score([staff])
    contexttools.TempoMark((1, 4), 60)(staff.select_leaves()[0])

    r'''
    \new Score <<
        \new Staff {
            \tempo 4=60
            c'4
            d'4
            \times 2/3 {
                e'4
                f'4
                g'4
            }
        }
    >>
    '''

    assert more(staff).get_timespan(in_seconds=True) == \
        timespantools.Timespan(0, 4)
    assert more(staff[0]).get_timespan(in_seconds=True) == \
        timespantools.Timespan(0, 1)
    assert more(staff[1]).get_timespan(in_seconds=True) == \
        timespantools.Timespan(1, 2)
    assert more(staff[-1]).get_timespan(in_seconds=True) == \
        timespantools.Timespan(2, 4)
