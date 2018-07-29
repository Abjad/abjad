import abjad


def test_Slur___eq___01():
    """
    Spanner is strict comparator.
    """

    spanner_1 = abjad.Slur()
    spanner_2 = abjad.Slur()

    assert not spanner_1 == spanner_2
