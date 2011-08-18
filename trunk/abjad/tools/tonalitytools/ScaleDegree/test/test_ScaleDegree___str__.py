from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree___str___01():

    assert str(tonalitytools.ScaleDegree(1)) == '1'
    assert str(tonalitytools.ScaleDegree('flat', 2)) == 'b2'
    assert str(tonalitytools.ScaleDegree('sharp', 4)) == '#4'
