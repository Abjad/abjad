# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RomanNumeral___repr___01():

    harmony = tonalanalysistools.RomanNumeral(1, 'major', 5, 0)
    assert repr(harmony) == 'IMajorTriadInRootPosition'

    harmony = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 2)
    assert repr(harmony) == 'VDominantSeventhInSecondInversion'

    harmony = tonalanalysistools.RomanNumeral(('flat', 2), 'major', 5, 1)
    assert repr(harmony) == 'FlatIIMajorTriadInFirstInversion'

    harmony = tonalanalysistools.RomanNumeral(1, 'minor', 5, 0)
    assert repr(harmony) == 'iMinorTriadInRootPosition'
