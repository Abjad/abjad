from abjad import *


def test_OctaveTranspositionMappingComponent_source_pitch_range_01():

    component = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
    assert component.source_pitch_range == pitchtools.PitchRange('[A0, C8]')
