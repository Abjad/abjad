from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree_apply_accidental_01():

    degree = tonalitytools.ScaleDegree('flat', 2)
    assert degree.apply_accidental('sharp') == tonalitytools.ScaleDegree(2)
    assert degree.apply_accidental('ss') == tonalitytools.ScaleDegree('sharp', 2)
