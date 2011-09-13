from abjad import *


def test_TextSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.TextSpanner()
    spanner_2 = spannertools.TextSpanner()

    assert not spanner_1 == spanner_2
