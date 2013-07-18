from abjad import *
from abjad.tools import tonalanalysistools


def test_ScaleDegree__init_by_scale_degree_01():

    degree = tonalanalysistools.ScaleDegree('flat', 2)
    new = tonalanalysistools.ScaleDegree(degree)

    assert new is not degree
    assert new.accidental == pitchtools.Accidental('flat')
    assert new.number == 2
