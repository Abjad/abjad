from abjad import *


def test_NamedChromaticPitch___float___01():
    '''Return chromatic pitch number of 12-ET named chromatic pitch as float.
    '''

    named_chromatic_pitch = pitchtools.NamedChromaticPitch(13)
    assert isinstance(float(named_chromatic_pitch), float)
    assert float(named_chromatic_pitch) == 13.0


def test_NamedChromaticPitch___float___02():
    '''Return chromatic pitch number of 24-ET named chromatic pitch as float.
    '''

    named_chromatic_pitch = pitchtools.NamedChromaticPitch(13.5)
    assert isinstance(float(named_chromatic_pitch), float)
    assert float(named_chromatic_pitch) == 13.5
