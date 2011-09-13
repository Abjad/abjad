from abjad import *


def test_NumberedChromaticPitch___sub___01():
    '''Subtract numbered chromatic pitch from numbered chromatic pitch.'''

    p = pitchtools.NumberedChromaticPitch(12)
    q = pitchtools.NumberedChromaticPitch(13)

    assert p - q == pitchtools.NumberedChromaticPitch(-1)
    assert q - p == pitchtools.NumberedChromaticPitch(1)


def test_NumberedChromaticPitch___sub___02():
    '''Subtract number from numbered chromatic pitch.'''

    p = pitchtools.NumberedChromaticPitch(12)

    assert p - 13 == pitchtools.NumberedChromaticPitch(-1)
