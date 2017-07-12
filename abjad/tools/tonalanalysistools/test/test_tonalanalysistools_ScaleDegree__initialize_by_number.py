# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree__initialize_by_number_01():

    degree = tonalanalysistools.ScaleDegree(2)
    assert degree.accidental == abjad.Accidental('')
    assert degree.number == 2


def test_tonalanalysistools_ScaleDegree__initialize_by_number_02():
    r'''Initialize from other scale degreeinstance.
    '''

    degree = tonalanalysistools.ScaleDegree(2)
    new = tonalanalysistools.ScaleDegree(degree)

    assert degree is not new
    assert new.number == 2
