from abjad import *


def test_GlissandoSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.GlissandoSpanner()
    spanner_2 = spannertools.GlissandoSpanner()

    assert not spanner_1 == spanner_2
