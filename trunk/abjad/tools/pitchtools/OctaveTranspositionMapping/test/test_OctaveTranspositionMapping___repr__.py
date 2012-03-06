from abjad import *
from abjad.tools.pitchtools.OctaveTranspositionMapping import OctaveTranspositionMapping


def test_OctaveTranspositionMapping___repr___01():
    '''Repr is evaluable.
    '''

    mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    mapping_2 = eval(repr(mapping_1))

    assert isinstance(mapping_1, pitchtools.OctaveTranspositionMapping)
    assert isinstance(mapping_2, pitchtools.OctaveTranspositionMapping)
    assert mapping_1 == mapping_2
