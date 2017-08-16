import abjad


def test_spannertools_Slur___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.Slur()
    spanner_2 = abjad.Slur()

    assert not spanner_1 == spanner_2
