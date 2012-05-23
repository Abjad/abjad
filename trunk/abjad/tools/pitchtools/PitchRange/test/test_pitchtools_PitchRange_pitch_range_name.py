from abjad import *


def test_pitchtools_PitchRange_pitch_range_name_01():

    pitch_range = pitchtools.PitchRange(-12, 36)
    assert pitch_range.pitch_range_name is None


def test_pitchtools_PitchRange_pitch_range_name_02():

    pitch_range = pitchtools.PitchRange(-12, 36, pitch_range_name='four-octave range')
    assert pitch_range.pitch_range_name == 'four-octave range'
