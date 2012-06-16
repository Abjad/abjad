from abjad import *


def test_pitchtools_PitchRange_storage_format_01():

    pitch_range = pitchtools.PitchRange('[A0, C8]')

    assert pitch_range.storage_format == "pitchtools.PitchRange(\n\t'[A0, C8]'\n\t)"
