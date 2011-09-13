from abjad import *


def test_StaffLinesSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.StaffLinesSpanner()
    spanner_2 = spannertools.StaffLinesSpanner()

    assert not spanner_1 == spanner_2
