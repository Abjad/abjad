# -*- encoding: utf-8 -*-
from abjad import *


def test_OctaveTranspositionMappingComponent___init___01():
    r'''Init from range and start pitch.
    '''

    component = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
    assert isinstance(component, pitchtools.OctaveTranspositionMappingComponent)


def test_OctaveTranspositionMappingComponent___init___02():
    r'''Init from pair.
    '''

    component = pitchtools.OctaveTranspositionMappingComponent(('[A0, C8]', 15))
    assert isinstance(component, pitchtools.OctaveTranspositionMappingComponent)


def test_OctaveTranspositionMappingComponent___init___03():
    r'''Init from instance.
    '''

    component_1 = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
    component_2 = pitchtools.OctaveTranspositionMappingComponent(component_1)
    assert isinstance(component_1, pitchtools.OctaveTranspositionMappingComponent)
    assert isinstance(component_2, pitchtools.OctaveTranspositionMappingComponent)


def test_OctaveTranspositionMappingComponent___init___04():
    r'''Init from string with number.
    '''

    component = pitchtools.OctaveTranspositionMappingComponent('[A0, C8] => 15')
    assert isinstance(component, pitchtools.OctaveTranspositionMappingComponent)


def test_OctaveTranspositionMappingComponent___init___05():
    r'''Init from string with pitch name.
    '''

    component = pitchtools.OctaveTranspositionMappingComponent('[A0, C8] => Eb5')
    assert isinstance(component, pitchtools.OctaveTranspositionMappingComponent)
