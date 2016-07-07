# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Tuplet_get_timespan_01():

    staff = Staff(r"c'4 d'4 \times 2/3 { e'4 f'4 g'4 }")
    leaves = select(staff).by_leaf()
    score = Score([staff])
    tempo = Tempo((1, 4), 60)
    attach(tempo, leaves[0])

    assert format(score) == stringtools.normalize(
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
        )

    assert inspect_(staff).get_timespan(in_seconds=True) == \
        timespantools.Timespan(0, 4)
    assert inspect_(staff[0]).get_timespan(in_seconds=True) == \
        timespantools.Timespan(0, 1)
    assert inspect_(staff[1]).get_timespan(in_seconds=True) == \
        timespantools.Timespan(1, 2)
    assert inspect_(staff[-1]).get_timespan(in_seconds=True) == \
        timespantools.Timespan(2, 4)
