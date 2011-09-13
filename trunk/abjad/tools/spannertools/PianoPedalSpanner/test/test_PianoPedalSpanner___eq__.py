from abjad import *


def test_PianoPedalSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.PianoPedalSpanner()
    spanner_2 = spannertools.PianoPedalSpanner()

    assert not spanner_1 == spanner_2
