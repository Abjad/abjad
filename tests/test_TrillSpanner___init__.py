import abjad


def test_TrillSpanner___init___01():
    """
    Initialize empty trill spanner.
    """

    trill = abjad.TrillSpanner()
    assert isinstance(trill, abjad.TrillSpanner)
