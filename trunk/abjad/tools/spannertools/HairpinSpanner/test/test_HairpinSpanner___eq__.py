from abjad import *


def test_HairpinSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.HairpinSpanner()
    spanner_2 = spannertools.HairpinSpanner()

    assert not spanner_1 == spanner_2
