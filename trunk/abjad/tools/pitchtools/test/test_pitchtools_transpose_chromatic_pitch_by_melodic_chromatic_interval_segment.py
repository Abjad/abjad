from abjad.tools.pitchtools import MelodicChromaticIntervalSegment
from abjad.tools.pitchtools import NamedChromaticPitch
from abjad.tools.pitchtools import NumberedChromaticPitch
from abjad.tools.pitchtools import transpose_chromatic_pitch_by_melodic_chromatic_interval_segment


def test_pitchtools_transpose_chromatic_pitch_by_melodic_chromatic_interval_segment_01():
    mcis = MelodicChromaticIntervalSegment([-2, 1, 1, -3, 0])
    nucp = NumberedChromaticPitch(0)
    result = transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(nucp, mcis)
    assert result == [
        NumberedChromaticPitch(-2),
        NumberedChromaticPitch(-1),
        NumberedChromaticPitch(0),
        NumberedChromaticPitch(-3),
        NumberedChromaticPitch(-3)
    ]
