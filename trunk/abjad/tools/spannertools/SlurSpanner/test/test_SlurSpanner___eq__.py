from abjad import *


def test_SlurSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.SlurSpanner()
    spanner_2 = spannertools.SlurSpanner()

    assert not spanner_1 == spanner_2
