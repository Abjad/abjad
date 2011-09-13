from abjad import *


def test_OctavationSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.OctavationSpanner()
    spanner_2 = spannertools.OctavationSpanner()

    assert not spanner_1 == spanner_2
