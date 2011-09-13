from abjad import *


def test_PhrasingSlurSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.PhrasingSlurSpanner()
    spanner_2 = spannertools.PhrasingSlurSpanner()

    assert not spanner_1 == spanner_2
