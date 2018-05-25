import abjad


def test_spannertools_TextSpanner___init___01():
    """
    Initialize empty text spanner.
    """

    spanner = abjad.TextSpanner()
    assert isinstance(spanner, abjad.TextSpanner)
