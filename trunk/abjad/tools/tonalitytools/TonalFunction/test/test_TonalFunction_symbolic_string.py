from abjad import *
from abjad.tools import tonalitytools


def test_TonalFunction_symbolic_string_01():

    t = tonalitytools.TonalFunction(5, 'dominant', 7, 0, (4, 3))
    assert t.symbolic_string == 'V7/4-3'

    t = tonalitytools.TonalFunction(2, 'minor', 7, 1)
    assert t.symbolic_string == 'ii6/5'

    t = tonalitytools.TonalFunction(1, 'major', 5, 1)
    assert t.symbolic_string == 'I6'
