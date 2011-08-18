from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree__init_by_pair_01():

    degree = tonalitytools.ScaleDegree(('flat', 2))

    assert degree.accidental == pitchtools.Accidental('flat')
    assert degree.number == 2
