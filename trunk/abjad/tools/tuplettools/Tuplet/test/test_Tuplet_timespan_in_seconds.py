from abjad import *


def test_Tuplet_timespan_in_seconds_01():

    staff = Staff(r"c'4 d'4 \times 2/3 { e'4 f'4 g'4 }")
    score = Score([staff])
    contexttools.TempoMark((1, 4), 60)(staff.leaves[0])

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

    assert staff.timespan_in_seconds == timespantools.Timespan(0, 4)
    assert staff[0].timespan_in_seconds == timespantools.Timespan(0, 1)
    assert staff[1].timespan_in_seconds == timespantools.Timespan(1, 2)
    assert staff[-1].timespan_in_seconds == timespantools.Timespan(2, 4)
