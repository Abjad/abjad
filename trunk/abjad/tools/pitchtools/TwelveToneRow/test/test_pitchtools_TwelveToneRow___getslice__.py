from abjad import *


def test_pitchtools_TwelveToneRow___getslice___01():
    '''Return numbered chromatic pitch-class segment on call to getslice.
    '''

    twelve_tone_row = pitchtools.TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])

    assert twelve_tone_row[:6] == pitchtools.NumberedChromaticPitchClassSegment([0, 1, 11, 9, 3, 6])
