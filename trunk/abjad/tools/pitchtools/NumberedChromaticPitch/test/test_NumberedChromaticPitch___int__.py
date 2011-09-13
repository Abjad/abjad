from abjad import *
import py.test


def test_NumberedChromaticPitch___int___01():
    '''Return chromatic pitch number of 12-ET numbered chromatic pitch as int.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedChromaticPitch(13)
    assert isinstance(int(numbered_chromatic_pitch), int)
    assert int(numbered_chromatic_pitch) == 13


def test_NumberedChromaticPitch___int___02():
    '''Raise type error on non-12-ET numbered chromatic pitch.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedChromaticPitch(13.5)
    assert py.test.raises(TypeError, 'int(numbered_chromatic_pitch)')
