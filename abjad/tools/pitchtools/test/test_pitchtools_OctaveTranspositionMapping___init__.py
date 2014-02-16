# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_OctaveTranspositionMapping___init___01():
    r'''Initialize from items.
    '''

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert isinstance(mapping, pitchtools.OctaveTranspositionMapping)


def test_pitchtools_OctaveTranspositionMapping___init___02():
    r'''Initialize from instance.
    '''

    mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    mapping_2 = pitchtools.OctaveTranspositionMapping(mapping_1)

    assert isinstance(mapping_1, pitchtools.OctaveTranspositionMapping)
    assert isinstance(mapping_2, pitchtools.OctaveTranspositionMapping)
    assert mapping_1 == mapping_2


def test_pitchtools_OctaveTranspositionMapping___init___03():
    r'''Initialize from named instance.
    '''

    mapping_1 = pitchtools.OctaveTranspositionMapping(
        [('[A0, C4)', 15), ('[C4, C8)', 27)],
        )
    mapping_2 = pitchtools.OctaveTranspositionMapping(mapping_1)

    assert isinstance(mapping_1, pitchtools.OctaveTranspositionMapping)
    assert isinstance(mapping_2, pitchtools.OctaveTranspositionMapping)
    assert mapping_1 == mapping_2


def test_pitchtools_OctaveTranspositionMapping___init___04():
    r'''Initializeempty.
    '''

    mapping = pitchtools.OctaveTranspositionMapping()
    assert isinstance(mapping, pitchtools.OctaveTranspositionMapping)

    mapping = pitchtools.OctaveTranspositionMapping([])
    assert isinstance(mapping, pitchtools.OctaveTranspositionMapping)
