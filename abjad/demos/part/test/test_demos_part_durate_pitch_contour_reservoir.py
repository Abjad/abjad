# -*- coding: utf-8 -*-
from abjad.demos import part


def test_demos_part_durate_pitch_contour_reservoir_01():

    pitch_contour_reservoir = part.create_pitch_contour_reservoir()
    shadowed_reservoir = part.shadow_pitch_contour_reservoir(
        pitch_contour_reservoir)
    durated_reservoir = part.durate_pitch_contour_reservoir(
        shadowed_reservoir)
