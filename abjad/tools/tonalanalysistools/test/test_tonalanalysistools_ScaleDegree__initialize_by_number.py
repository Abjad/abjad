# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_ScaleDegree__initialize_by_number_01():

    degree = tonalanalysistools.ScaleDegree(2)
    assert degree.accidental == pitchtools.Accidental('')
    assert degree.number == 2


def test_tonalanalysistools_ScaleDegree__initialize_by_number_02():
    r'''Initialize from other scale degreeinstance.
    '''

    degree = tonalanalysistools.ScaleDegree(2)
    new = tonalanalysistools.ScaleDegree(degree)

    assert degree is not new
    assert new.number == 2
