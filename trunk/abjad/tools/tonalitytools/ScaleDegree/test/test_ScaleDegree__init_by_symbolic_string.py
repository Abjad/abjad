from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree__init_by_symbolic_string_01():

    scale_degree = tonalitytools.ScaleDegree('I')
    assert scale_degree == tonalitytools.ScaleDegree(1)

    scale_degree = tonalitytools.ScaleDegree('i')
    assert scale_degree == tonalitytools.ScaleDegree(1)

    scale_degree = tonalitytools.ScaleDegree('bII')
    assert scale_degree == tonalitytools.ScaleDegree('flat', 2)

    scale_degree = tonalitytools.ScaleDegree('bii')
    assert scale_degree == tonalitytools.ScaleDegree('flat', 2)


def test_ScaleDegree__init_by_symbolic_string_02():

    scale_degree = tonalitytools.ScaleDegree('1')
    assert scale_degree == tonalitytools.ScaleDegree(1)

    scale_degree = tonalitytools.ScaleDegree('b2')
    assert scale_degree == tonalitytools.ScaleDegree('flat', 2)

    scale_degree = tonalitytools.ScaleDegree('#4')
    assert scale_degree == tonalitytools.ScaleDegree('sharp', 4)
