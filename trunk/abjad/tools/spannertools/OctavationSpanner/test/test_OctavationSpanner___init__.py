from abjad import *


def test_OctavationSpanner___init___01():
    '''Init empty octavation spanner.
    '''

    octavation = spannertools.OctavationSpanner()
    assert isinstance(octavation, spannertools.OctavationSpanner)
