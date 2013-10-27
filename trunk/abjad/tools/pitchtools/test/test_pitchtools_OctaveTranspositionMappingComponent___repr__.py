# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools.OctaveTranspositionMappingComponent \
	import OctaveTranspositionMappingComponent


def test_pitchtools_OctaveTranspositionMappingComponent___repr___01():
    r'''Reprs are evaluable.
    '''

    component_1 = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
    component_2 = eval(repr(component_1))

    assert component_1 == component_2
