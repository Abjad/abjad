from abjad import *
from abjad.tools import tonalitytools


def test_TonalFunction_suspension_01():

    t = tonalitytools.TonalFunction(5, 'major', 5, 0, (4, 3))

    assert t.suspension == tonalitytools.SuspensionIndicator(4, 3)
    assert t.suspension.start == tonalitytools.ScaleDegree(4)
    assert t.suspension.stop == tonalitytools.ScaleDegree(3)
