from abjad import *


def test_pitchtools_PitchRange__repr_with_tools_package_01():

    pitch_range = pitchtools.PitchRange('[A0, C8]')

    assert pitch_range._repr_with_tools_package == "pitchtools.PitchRange('[A0, C8]')"
