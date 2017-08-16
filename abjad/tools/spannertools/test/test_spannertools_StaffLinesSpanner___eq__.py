import abjad


def test_spannertools_StaffLinesSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.StaffLinesSpanner()
    spanner_2 = abjad.StaffLinesSpanner()

    assert not spanner_1 == spanner_2
