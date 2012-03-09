from abjad import *


def test_pitchtools_PitchRange__fully_qualified_repr_01():

    pitch_range = pitchtools.PitchRange('[A0, C8]')

    assert pitch_range._fully_qualified_repr == "pitchtools.PitchRange('[A0, C8]')"
