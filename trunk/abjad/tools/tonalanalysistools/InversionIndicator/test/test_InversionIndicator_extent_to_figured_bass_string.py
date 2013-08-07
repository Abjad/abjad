# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_InversionIndicator_extent_to_figured_bass_string_01():

    inversion_indicator = tonalanalysistools.InversionIndicator(0)
    assert inversion_indicator.extent_to_figured_bass_string(5) == ''
    assert inversion_indicator.extent_to_figured_bass_string(7) == '7'

    inversion_indicator = tonalanalysistools.InversionIndicator(1)
    assert inversion_indicator.extent_to_figured_bass_string(5) == '6'
    assert inversion_indicator.extent_to_figured_bass_string(7) == '6/5'

    inversion_indicator = tonalanalysistools.InversionIndicator(2)
    assert inversion_indicator.extent_to_figured_bass_string(5) == '6/4'
    assert inversion_indicator.extent_to_figured_bass_string(7) == '4/3'

    inversion_indicator = tonalanalysistools.InversionIndicator(3)
    assert inversion_indicator.extent_to_figured_bass_string(7) == '4/2'
