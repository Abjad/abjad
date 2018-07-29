import abjad


def test_Spanner___eq___01():
    """
    Spanner is strict comparator.
    """

    assert not abjad.Spanner() == abjad.Spanner()
