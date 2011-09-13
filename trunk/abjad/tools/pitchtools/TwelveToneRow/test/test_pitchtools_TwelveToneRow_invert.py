from abjad import *


def test_pitchtools_TwelveToneRow_invert_01():

    row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
    inversion = pitchtools.TwelveToneRow([2, 0, 10, 6, 4, 5, 7, 9, 11, 3, 8, 1])

    assert row.invert() == inversion
