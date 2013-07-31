from abjad import *


def test_OctaveTranspositionMapping___contains___01():
    r'''Works with components.
    '''

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert pitchtools.OctaveTranspositionMappingComponent('[A0, C4)', 15) in mapping


def test_OctaveTranspositionMapping___contains___02():
    r'''Works with component tokens.
    '''

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert ('[A0, C4)', 15) in mapping
