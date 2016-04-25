# -*- coding: utf-8 -*-
from abjad import *
from abjad.demos import part


def test_demos_part_shadow_pitch_contour_reservoir_01():

    pitch_contour_reservoir = part.create_pitch_contour_reservoir()
    shadowed_reservoir = part.shadow_pitch_contour_reservoir(
        pitch_contour_reservoir)

    assert sorted(pitch_contour_reservoir.keys()) == \
        sorted(shadowed_reservoir.keys())

    for key in pitch_contour_reservoir:
        assert isinstance(shadowed_reservoir[key], tuple)
        assert len(pitch_contour_reservoir[key]) == \
            len(shadowed_reservoir[key])
