from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree_symbolic_string_01():

    assert tonalitytools.ScaleDegree(1).symbolic_string == 'I'
    assert tonalitytools.ScaleDegree('flat', 2).symbolic_string == 'bII'
    assert tonalitytools.ScaleDegree(3).symbolic_string == 'III'
    assert tonalitytools.ScaleDegree('sharp', 4).symbolic_string == '#IV'
    assert tonalitytools.ScaleDegree(5).symbolic_string == 'V'
    assert tonalitytools.ScaleDegree('flat', 6).symbolic_string == 'bVI'
    assert tonalitytools.ScaleDegree('flat', 7).symbolic_string == 'bVII'
