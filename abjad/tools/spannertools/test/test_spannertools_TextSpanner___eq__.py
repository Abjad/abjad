import abjad


def test_spannertools_TextSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.TextSpanner()
    spanner_2 = abjad.TextSpanner()

    assert not spanner_1 == spanner_2
