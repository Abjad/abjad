from abjad import *
from abjad.tools import tonalanalysistools


def test_ScaleDegree__init_by_number_01():

    degree = tonalanalysistools.ScaleDegree(2)
    assert degree.accidental == pitchtools.Accidental('')
    assert degree.number == 2


def test_ScaleDegree__init_by_number_02():
    '''Init from other scale degree instance.
    '''

    degree = tonalanalysistools.ScaleDegree(2)
    new = tonalanalysistools.ScaleDegree(degree)

    assert degree is not new
    assert new.number == 2
