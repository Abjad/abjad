from abjad import *


def test_DecrescendoSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.DecrescendoSpanner()
    spanner_2 = spannertools.DecrescendoSpanner()

    assert not spanner_1 == spanner_2
