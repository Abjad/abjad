# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordInversion_extent_to_figured_bass_string_01():

    chord_inversion = tonalanalysistools.ChordInversion(0)
    assert chord_inversion.extent_to_figured_bass_string(5) == ''
    assert chord_inversion.extent_to_figured_bass_string(7) == '7'

    chord_inversion = tonalanalysistools.ChordInversion(1)
    assert chord_inversion.extent_to_figured_bass_string(5) == '6'
    assert chord_inversion.extent_to_figured_bass_string(7) == '6/5'

    chord_inversion = tonalanalysistools.ChordInversion(2)
    assert chord_inversion.extent_to_figured_bass_string(5) == '6/4'
    assert chord_inversion.extent_to_figured_bass_string(7) == '4/3'

    chord_inversion = tonalanalysistools.ChordInversion(3)
    assert chord_inversion.extent_to_figured_bass_string(7) == '4/2'
