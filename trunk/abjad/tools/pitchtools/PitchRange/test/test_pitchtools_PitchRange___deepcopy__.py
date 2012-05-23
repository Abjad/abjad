from abjad import *
import copy


def test_pitchtools_PitchRange___deepcopy___01():

    pitch_range_1 = pitchtools.PitchRange(-39, 48)
    pitch_range_2 = copy.deepcopy(pitch_range_1)

    assert pitch_range_1 == pitch_range_2
    assert pitch_range_1 is not pitch_range_2
