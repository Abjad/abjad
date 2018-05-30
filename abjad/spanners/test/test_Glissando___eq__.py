import abjad


def test_Glissando___eq___01():
    """
    Spanner is strict comparator.
    """

    spanner_1 = abjad.Glissando()
    spanner_2 = abjad.Glissando()

    assert not spanner_1 == spanner_2
