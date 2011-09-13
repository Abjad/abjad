from abjad import *


def test_NumberedChromaticPitch___add___01():
    '''Add numbered chromatic pitch to numbered chromatic pitch.'''

    p = pitchtools.NumberedChromaticPitch(12)
    q = pitchtools.NumberedChromaticPitch(13)

    assert p + q == pitchtools.NumberedChromaticPitch(25)


def test_NumberedChromaticPitch___add___02():
    '''Add number to numbered chromatic pitch.'''

    p = pitchtools.NumberedChromaticPitch(12)

    assert p + 13 == pitchtools.NumberedChromaticPitch(25)
