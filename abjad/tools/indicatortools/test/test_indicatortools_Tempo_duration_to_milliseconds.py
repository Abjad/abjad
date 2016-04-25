# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Tempo_duration_to_milliseconds_01():

    beat = Fraction(1, 4)
    tempo = Tempo((1, 4), 60)
    assert tempo.duration_to_milliseconds(beat) == 1000


def test_indicatortools_Tempo_duration_to_milliseconds_02():

    beat = Fraction(1, 4)
    tempo = Tempo((1, 4), 55)
    assert tempo.duration_to_milliseconds(beat) == Fraction(60, 55) * 1000


def test_indicatortools_Tempo_duration_to_milliseconds_03():

    beat = Fraction(3, 4)
    tempo = Tempo((1, 4), 60)
    assert tempo.duration_to_milliseconds(beat) == 3000
