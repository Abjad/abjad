# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordInversion_extent_to_figured_bass_string_01():

    inversion_indicator = tonalanalysistools.ChordInversion(0)
    assert inversion_indicator.extent_to_figured_bass_string(5) == ''
    assert inversion_indicator.extent_to_figured_bass_string(7) == '7'

    inversion_indicator = tonalanalysistools.ChordInversion(1)
    assert inversion_indicator.extent_to_figured_bass_string(5) == '6'
    assert inversion_indicator.extent_to_figured_bass_string(7) == '6/5'

    inversion_indicator = tonalanalysistools.ChordInversion(2)
    assert inversion_indicator.extent_to_figured_bass_string(5) == '6/4'
    assert inversion_indicator.extent_to_figured_bass_string(7) == '4/3'

    inversion_indicator = tonalanalysistools.ChordInversion(3)
    assert inversion_indicator.extent_to_figured_bass_string(7) == '4/2'
