import abjad


def test_OctavationSpanner___init___01():
    """
    Initialize empty octavation spanner.
    """

    octavation = abjad.OctavationSpanner()
    assert isinstance(octavation, abjad.OctavationSpanner)
