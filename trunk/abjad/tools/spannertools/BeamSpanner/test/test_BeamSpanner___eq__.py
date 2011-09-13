from abjad import *


def test_BeamSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.BeamSpanner()
    spanner_2 = spannertools.BeamSpanner()

    assert not spanner_1 == spanner_2
