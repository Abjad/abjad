# -*- coding: utf-8 -*-
from abjad import *
from abjad.demos import part


def test_demos_part_create_pitch_contour_reservoir_01():

    reservoir = part.create_pitch_contour_reservoir()

    assert isinstance(reservoir, dict)
    for key, value in reservoir.items():
        assert isinstance(key, str)
        assert isinstance(value, tuple)
        assert len(value)
