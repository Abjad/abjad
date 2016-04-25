# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree__initialize_by_symbolic_string_01():

    scale_degree = tonalanalysistools.ScaleDegree('I')
    assert scale_degree == tonalanalysistools.ScaleDegree(1)

    scale_degree = tonalanalysistools.ScaleDegree('i')
    assert scale_degree == tonalanalysistools.ScaleDegree(1)

    scale_degree = tonalanalysistools.ScaleDegree('bII')
    assert scale_degree == tonalanalysistools.ScaleDegree('flat', 2)

    scale_degree = tonalanalysistools.ScaleDegree('bii')
    assert scale_degree == tonalanalysistools.ScaleDegree('flat', 2)


def test_tonalanalysistools_ScaleDegree__initialize_by_symbolic_string_02():

    scale_degree = tonalanalysistools.ScaleDegree('1')
    assert scale_degree == tonalanalysistools.ScaleDegree(1)

    scale_degree = tonalanalysistools.ScaleDegree('b2')
    assert scale_degree == tonalanalysistools.ScaleDegree('flat', 2)

    scale_degree = tonalanalysistools.ScaleDegree('#4')
    assert scale_degree == tonalanalysistools.ScaleDegree('sharp', 4)
