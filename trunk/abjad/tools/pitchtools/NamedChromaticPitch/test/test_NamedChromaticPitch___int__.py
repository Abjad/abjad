from abjad import *
import py.test


def test_NamedChromaticPitch___int___01():
    '''Return chromatic pitch number of 12-ET named chromatic pitch as int.
    '''

    named_chromatic_pitch = pitchtools.NamedChromaticPitch(13)
    assert isinstance(int(named_chromatic_pitch), int)
    assert int(named_chromatic_pitch) == 13


def test_NamedChromaticPitch___int___02():
    '''Raise type error on non-12-ET named chromatic pitch.
    '''

    named_chromatic_pitch = pitchtools.NamedChromaticPitch(13.5)
    assert py.test.raises(TypeError, 'int(named_chromatic_pitch)')
