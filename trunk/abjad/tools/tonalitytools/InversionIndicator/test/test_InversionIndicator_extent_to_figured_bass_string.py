from abjad import *
from abjad.tools import tonalitytools


def test_InversionIndicator_extent_to_figured_bass_string_01():

    t = tonalitytools.InversionIndicator(0)
    assert t.extent_to_figured_bass_string(5) == ''
    assert t.extent_to_figured_bass_string(7) == '7'

    t = tonalitytools.InversionIndicator(1)
    assert t.extent_to_figured_bass_string(5) == '6'
    assert t.extent_to_figured_bass_string(7) == '6/5'

    t = tonalitytools.InversionIndicator(2)
    assert t.extent_to_figured_bass_string(5) == '6/4'
    assert t.extent_to_figured_bass_string(7) == '4/3'

    t = tonalitytools.InversionIndicator(3)
    assert t.extent_to_figured_bass_string(7) == '4/2'
