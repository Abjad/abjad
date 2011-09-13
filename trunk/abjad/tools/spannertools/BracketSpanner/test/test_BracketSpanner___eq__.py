from abjad import *


def test_BracketSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.BracketSpanner()
    spanner_2 = spannertools.BracketSpanner()

    assert not spanner_1 == spanner_2
