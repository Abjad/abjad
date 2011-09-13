from abjad import *


def test_Spanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.Spanner()
    spanner_2 = spannertools.Spanner()

    assert not spanner_1 == spanner_2
