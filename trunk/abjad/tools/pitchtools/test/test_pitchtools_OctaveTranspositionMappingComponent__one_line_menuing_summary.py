# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_OctaveTranspositionMappingComponent__one_line_menuing_summary_01():

    mapping_component = pitchtools.OctaveTranspositionMappingComponent('[A0, F#4]', 22)
    assert mapping_component._one_line_menuing_summary == '[A0, F#4] => 22'
