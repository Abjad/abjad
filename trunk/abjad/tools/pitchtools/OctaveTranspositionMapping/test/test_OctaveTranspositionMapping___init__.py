from abjad import *


def test_OctaveTranspositionMapping___init___01():
    '''Init from tokens.
    '''

    mapping = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert isinstance(mapping, pitchtools.OctaveTranspositionMapping)


def test_OctaveTranspositionMapping___init___02():
    '''Init from instance.
    '''

    mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    mapping_2 = pitchtools.OctaveTranspositionMapping(mapping_1)

    assert isinstance(mapping_1, pitchtools.OctaveTranspositionMapping)
    assert isinstance(mapping_2, pitchtools.OctaveTranspositionMapping)
    assert mapping_1 == mapping_2


def test_OctaveTranspositionMapping___init___03():
    '''Init from named instance.
    '''

    mapping_1 = pitchtools.OctaveTranspositionMapping(
        [('[A0, C4)', 15), ('[C4, C8)', 27)], 
        name='foo')
    mapping_2 = pitchtools.OctaveTranspositionMapping(mapping_1)

    assert isinstance(mapping_1, pitchtools.OctaveTranspositionMapping)
    assert isinstance(mapping_2, pitchtools.OctaveTranspositionMapping)
    assert mapping_1 == mapping_2


def test_OctaveTranspositionMapping___init___04():
    '''Init empty.
    '''

    mapping = pitchtools.OctaveTranspositionMapping()
    assert isinstance(mapping, pitchtools.OctaveTranspositionMapping)

    mapping = pitchtools.OctaveTranspositionMapping([])
    assert isinstance(mapping, pitchtools.OctaveTranspositionMapping)
