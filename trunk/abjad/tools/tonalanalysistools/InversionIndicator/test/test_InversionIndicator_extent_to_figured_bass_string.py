from abjad import *
from abjad.tools import tonalanalysistools


def test_InversionIndicator_extent_to_figured_bass_string_01():

    t = tonalanalysistools.InversionIndicator(0)
    assert t.extent_to_figured_bass_string(5) == ''
    assert t.extent_to_figured_bass_string(7) == '7'

    t = tonalanalysistools.InversionIndicator(1)
    assert t.extent_to_figured_bass_string(5) == '6'
    assert t.extent_to_figured_bass_string(7) == '6/5'

    t = tonalanalysistools.InversionIndicator(2)
    assert t.extent_to_figured_bass_string(5) == '6/4'
    assert t.extent_to_figured_bass_string(7) == '4/3'

    t = tonalanalysistools.InversionIndicator(3)
    assert t.extent_to_figured_bass_string(7) == '4/2'
