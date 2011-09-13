from abjad import *


def test_HiddenStaffSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.HiddenStaffSpanner()
    spanner_2 = spannertools.HiddenStaffSpanner()

    assert not spanner_1 == spanner_2
