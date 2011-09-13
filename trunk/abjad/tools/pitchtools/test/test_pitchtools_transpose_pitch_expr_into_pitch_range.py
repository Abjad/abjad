from abjad import *


def test_pitchtools_transpose_pitch_expr_into_pitch_range_01():

    pitch_range = pitchtools.PitchRange(0, 12)

    assert pitchtools.transpose_pitch_expr_into_pitch_range(-2, pitch_range) == 10
    assert pitchtools.transpose_pitch_expr_into_pitch_range(-1, pitch_range) == 11
    assert pitchtools.transpose_pitch_expr_into_pitch_range(0, pitch_range) == 0
    assert pitchtools.transpose_pitch_expr_into_pitch_range(1, pitch_range) == 1
    assert pitchtools.transpose_pitch_expr_into_pitch_range(11, pitch_range) == 11
    assert pitchtools.transpose_pitch_expr_into_pitch_range(12, pitch_range) == 12
    assert pitchtools.transpose_pitch_expr_into_pitch_range(13, pitch_range) == 1


def test_pitchtools_transpose_pitch_expr_into_pitch_range_02():

    pitch_range = pitchtools.PitchRange(0, 12)

    assert pitchtools.transpose_pitch_expr_into_pitch_range([-2, -1, 13, 14], pitch_range) == [10, 11, 1, 2]
