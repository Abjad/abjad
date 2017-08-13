import abjad


def test_spannertools_Glissando___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.Glissando()
    spanner_2 = abjad.Glissando()

    assert not spanner_1 == spanner_2
