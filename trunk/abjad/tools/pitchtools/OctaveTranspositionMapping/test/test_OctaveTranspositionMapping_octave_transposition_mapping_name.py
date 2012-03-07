from abjad import *


def test_OctaveTranspositionMapping_octave_transposition_mapping_name_01():

    mapping = pitchtools.OctaveTranspositionMapping()
    assert mapping.octave_transposition_mapping_name is None

    mapping.octave_transposition_mapping_name = 'lower register mapping #2'
    assert mapping.octave_transposition_mapping_name == 'lower register mapping #2'
