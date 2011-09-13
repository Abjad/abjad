from abjad import *


def test_DynamicTextSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.DynamicTextSpanner()
    spanner_2 = spannertools.DynamicTextSpanner()

    assert not spanner_1 == spanner_2
