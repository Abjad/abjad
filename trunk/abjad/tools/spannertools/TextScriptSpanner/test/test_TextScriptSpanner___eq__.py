from abjad import *


def test_TextScriptSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.TextScriptSpanner()
    spanner_2 = spannertools.TextScriptSpanner()

    assert not spanner_1 == spanner_2
