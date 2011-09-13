from abjad import *


def test_pitchtools_TwelveToneRow___rmul___01():
    '''Return numbered chromatic pitch-class segment on calls to mul.
    '''

    twelve_tone_row = pitchtools.TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])
    result = 2 * twelve_tone_row

    assert result == pitchtools.NumberedChromaticPitchClassSegment([
        0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8,
        0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])
