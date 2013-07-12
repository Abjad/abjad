from abjad import *


def test_MeasuredComplexBeamSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.MeasuredComplexBeamSpanner()
    spanner_2 = spannertools.MeasuredComplexBeamSpanner()

    assert not spanner_1 == spanner_2
