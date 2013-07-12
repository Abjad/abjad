from abjad import *


def test_ComplexBeamSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.ComplexBeamSpanner()
    spanner_2 = spannertools.ComplexBeamSpanner()

    assert not spanner_1 == spanner_2
