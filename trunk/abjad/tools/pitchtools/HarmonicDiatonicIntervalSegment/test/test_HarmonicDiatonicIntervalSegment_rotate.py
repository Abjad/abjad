from abjad import *


def test_HarmonicDiatonicIntervalSegment_rotate_01():
    '''Rotate right.'''

    hdig = pitchtools.HarmonicDiatonicIntervalSegment([
        pitchtools.HarmonicDiatonicInterval('minor', 2),
        pitchtools.HarmonicDiatonicInterval('major', 2),
        pitchtools.HarmonicDiatonicInterval('minor', 3),
        pitchtools.HarmonicDiatonicInterval('major', 3)])

    rotated = hdig.rotate(1)

    new = pitchtools.HarmonicDiatonicIntervalSegment([
        pitchtools.HarmonicDiatonicInterval('major', 3),
        pitchtools.HarmonicDiatonicInterval('minor', 2),
        pitchtools.HarmonicDiatonicInterval('major', 2),
        pitchtools.HarmonicDiatonicInterval('minor', 3)])

    assert rotated == new


def test_HarmonicDiatonicIntervalSegment_rotate_02():
    '''Rotate left.'''

    hdig = pitchtools.HarmonicDiatonicIntervalSegment([
        pitchtools.HarmonicDiatonicInterval('minor', 2),
        pitchtools.HarmonicDiatonicInterval('major', 2),
        pitchtools.HarmonicDiatonicInterval('minor', 3),
        pitchtools.HarmonicDiatonicInterval('major', 3)])

    rotated = hdig.rotate(-1)

    new = pitchtools.HarmonicDiatonicIntervalSegment([
        pitchtools.HarmonicDiatonicInterval('major', 2),
        pitchtools.HarmonicDiatonicInterval('minor', 3),
        pitchtools.HarmonicDiatonicInterval('major', 3),
        pitchtools.HarmonicDiatonicInterval('minor', 2)])

    assert rotated == new
