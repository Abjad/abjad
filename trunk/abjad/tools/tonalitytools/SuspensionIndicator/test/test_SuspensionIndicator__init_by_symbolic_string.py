from abjad import *
from abjad.tools import tonalitytools


def test_SuspensionIndicator__init_by_symbolic_string_01():

    t = tonalitytools.SuspensionIndicator('4-3')
    assert t.start == tonalitytools.ScaleDegree(4)
    assert t.stop == tonalitytools.ScaleDegree(3)

    t = tonalitytools.SuspensionIndicator('b2-1')
    assert t.start == tonalitytools.ScaleDegree('flat', 2)
    assert t.stop == tonalitytools.ScaleDegree(1)
