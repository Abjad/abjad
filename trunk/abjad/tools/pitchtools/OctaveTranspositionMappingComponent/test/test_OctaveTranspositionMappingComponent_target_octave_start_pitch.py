from abjad import *


def test_OctaveTranspositionMappingComponent_target_octave_start_pitch_01():

    component = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
    assert component.target_octave_start_pitch == pitchtools.NumberedChromaticPitch(15)
