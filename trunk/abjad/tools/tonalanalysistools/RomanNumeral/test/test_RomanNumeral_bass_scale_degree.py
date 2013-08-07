# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_RomanNumeral_bass_scale_degree_01():

    romannumeral = tonalanalysistools.RomanNumeral(5, 'major', 5, 0)
    assert romannumeral.bass_scale_degree == tonalanalysistools.ScaleDegree(5)

    romannumeral = tonalanalysistools.RomanNumeral(5, 'major', 5, 1)
    assert romannumeral.bass_scale_degree == tonalanalysistools.ScaleDegree(7)

    romannumeral = tonalanalysistools.RomanNumeral(5, 'major', 5, 2)
    assert romannumeral.bass_scale_degree == tonalanalysistools.ScaleDegree(2)


def test_RomanNumeral_bass_scale_degree_02():

    t = tonalanalysistools.RomanNumeral(5, 'major', 7, 0)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(5)

    t = tonalanalysistools.RomanNumeral(5, 'major', 7, 1)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(7)

    t = tonalanalysistools.RomanNumeral(5, 'major', 7, 2)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(2)

    t = tonalanalysistools.RomanNumeral(5, 'major', 7, 3)
    assert t.bass_scale_degree == tonalanalysistools.ScaleDegree(4)
