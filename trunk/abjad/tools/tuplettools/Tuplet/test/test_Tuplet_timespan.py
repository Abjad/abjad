# -*- encoding: utf-8 -*-
from abjad import *


def test_Tuplet_timespan_01():

    staff = Staff(r"c'4 d'4 \times 2/3 { e'4 f'4 g'4 }")

    r'''
    \new Staff {
        c'4
        d'4
        \times 2/3 {
            e'4
            f'4
            g'4
        }
    }
    '''

    assert more(staff).get_timespan() == timespantools.Timespan(0, 1)
    assert more(staff[0]).get_timespan() == timespantools.Timespan(0, (1, 4))
    assert more(staff[1]).get_timespan() == timespantools.Timespan((1, 4), (1, 2))
    assert more(staff[-1]).get_timespan() == timespantools.Timespan((1, 2), 1)
