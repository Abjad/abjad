from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitchSet


def test_NamedChromaticPitchSet___repr___01():
    '''Named chromatic pitch set repr is evaluable.
    '''

    ncps =['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_chromatic_pitch_set_1 = pitchtools.NamedChromaticPitchSet(ncps)
    named_chromatic_pitch_set_2 = eval(repr(named_chromatic_pitch_set_1))

    assert isinstance(named_chromatic_pitch_set_1, pitchtools.NamedChromaticPitchSet)
    assert isinstance(named_chromatic_pitch_set_2, pitchtools.NamedChromaticPitchSet)
