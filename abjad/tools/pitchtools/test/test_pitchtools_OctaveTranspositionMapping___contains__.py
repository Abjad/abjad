# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_OctaveTranspositionMapping___contains___01():
    r'''Works with components.
    '''

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert pitchtools.OctaveTranspositionMappingComponent('[A0, C4)', 15) in mapping


def test_pitchtools_OctaveTranspositionMapping___contains___02():
    r'''Works with component items.
    '''

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert ('[A0, C4)', 15) in mapping
