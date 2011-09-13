from abjad import *


def test_MetricGridSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.MetricGridSpanner()
    spanner_2 = spannertools.MetricGridSpanner()

    assert not spanner_1 == spanner_2
