from abjad import *


def test_quantizationtools_tempo_scaled_duration_to_milliseconds_01():
    beat = Fraction(1, 4)
    tempo = contexttools.TempoMark((1, 4), 60)
    assert quantizationtools.tempo_scaled_duration_to_milliseconds(beat, tempo) == 1000


def test_quantizationtools_tempo_scaled_duration_to_milliseconds_02():
    beat = Fraction(1, 4)
    tempo = contexttools.TempoMark((1, 4), 55)
    assert quantizationtools.tempo_scaled_duration_to_milliseconds(beat, tempo) == Fraction(60, 55) * 1000


def test_quantizationtools_tempo_scaled_duration_to_milliseconds_03():
    beat = Fraction(3, 4)
    tempo = contexttools.TempoMark((1, 4), 60)
    assert quantizationtools.tempo_scaled_duration_to_milliseconds(beat, tempo) == 3000
