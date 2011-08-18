from abjad import *
from abjad.tools import tonalitytools


def test_TonalFunction_bass_scale_degree_01():

    t = tonalitytools.TonalFunction(5, 'major', 5, 0)
    assert t.bass_scale_degree == tonalitytools.ScaleDegree(5)

    t = tonalitytools.TonalFunction(5, 'major', 5, 1)
    assert t.bass_scale_degree == tonalitytools.ScaleDegree(7)

    t = tonalitytools.TonalFunction(5, 'major', 5, 2)
    assert t.bass_scale_degree == tonalitytools.ScaleDegree(2)


def test_TonalFunction_bass_scale_degree_02():

    t = tonalitytools.TonalFunction(5, 'major', 7, 0)
    assert t.bass_scale_degree == tonalitytools.ScaleDegree(5)

    t = tonalitytools.TonalFunction(5, 'major', 7, 1)
    assert t.bass_scale_degree == tonalitytools.ScaleDegree(7)

    t = tonalitytools.TonalFunction(5, 'major', 7, 2)
    assert t.bass_scale_degree == tonalitytools.ScaleDegree(2)

    t = tonalitytools.TonalFunction(5, 'major', 7, 3)
    assert t.bass_scale_degree == tonalitytools.ScaleDegree(4)
