# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_TonalFunction_bass_scale_degree_01():

    t = tonalanalysistools.TonalFunction(5, 'major', 5, 0)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(5)

    t = tonalanalysistools.TonalFunction(5, 'major', 5, 1)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(7)

    t = tonalanalysistools.TonalFunction(5, 'major', 5, 2)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(2)


def test_TonalFunction_bass_scale_degree_02():

    t = tonalanalysistools.TonalFunction(5, 'major', 7, 0)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(5)

    t = tonalanalysistools.TonalFunction(5, 'major', 7, 1)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(7)

    t = tonalanalysistools.TonalFunction(5, 'major', 7, 2)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(2)

    t = tonalanalysistools.TonalFunction(5, 'major', 7, 3)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(4)
