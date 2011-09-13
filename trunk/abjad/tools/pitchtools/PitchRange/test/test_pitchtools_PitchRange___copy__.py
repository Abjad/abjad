from abjad import *
import copy


def test_pitchtools_PitchRange___copy___01():

    pitch_range_1 = pitchtools.PitchRange(-39, 48)
    pitch_range_2 = copy.copy(pitch_range_1)

    assert pitch_range_1 == pitch_range_2
    assert pitch_range_1 is not pitch_range_2
