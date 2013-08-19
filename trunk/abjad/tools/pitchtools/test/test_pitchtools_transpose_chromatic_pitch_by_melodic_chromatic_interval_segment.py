# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools import MelodicChromaticIntervalSegment
from abjad.tools.pitchtools import NamedPitch
from abjad.tools.pitchtools import NumberedPitch
from abjad.tools.pitchtools \
	import transpose_chromatic_pitch_by_melodic_chromatic_interval_segment


def test_pitchtools_transpose_chromatic_pitch_by_melodic_chromatic_interval_segment_01():
    mcis = MelodicChromaticIntervalSegment([-2, 1, 1, -3, 0])
    nucp = NumberedPitch(0)
    result = transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(nucp, mcis)
    assert result == [
        NumberedPitch(-2),
        NumberedPitch(-1),
        NumberedPitch(0),
        NumberedPitch(-3),
        NumberedPitch(-3)
    ]
