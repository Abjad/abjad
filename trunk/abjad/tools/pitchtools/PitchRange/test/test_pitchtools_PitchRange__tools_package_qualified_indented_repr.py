from abjad import *


def test_pitchtools_PitchRange__tools_package_qualified_indented_repr_01():

    pitch_range = pitchtools.PitchRange('[A0, C8]')

    assert pitch_range._tools_package_qualified_repr == "pitchtools.PitchRange('[A0, C8]')"
    assert pitch_range._tools_package_qualified_indented_repr == "pitchtools.PitchRange(\n\t'[A0, C8]'\n\t)"
