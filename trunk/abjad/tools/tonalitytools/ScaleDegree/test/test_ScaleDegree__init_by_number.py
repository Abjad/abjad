from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree__init_by_number_01():

    degree = tonalitytools.ScaleDegree(2)
    assert degree.accidental == pitchtools.Accidental('')
    assert degree.number == 2


def test_ScaleDegree__init_by_number_02():
    '''Init from other scale degree instance.'''

    degree = tonalitytools.ScaleDegree(2)
    new = tonalitytools.ScaleDegree(degree)

    assert degree is not new
    assert new.number == 2
