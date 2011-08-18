from abjad import *
from abjad.tools import tonalitytools


def test_TonalFunction___repr___01():

    harmony = tonalitytools.TonalFunction(1, 'major', 5, 0)
    assert repr(harmony) == 'IMajorTriadInRootPosition'

    harmony = tonalitytools.TonalFunction(5, 'dominant', 7, 2)
    assert repr(harmony) == 'VDominantSeventhInSecondInversion'

    harmony = tonalitytools.TonalFunction(('flat', 2), 'major', 5, 1)
    assert repr(harmony) == 'FlatIIMajorTriadInFirstInversion'

    harmony = tonalitytools.TonalFunction(1, 'minor', 5, 0)
    assert repr(harmony) == 'iMinorTriadInRootPosition'
