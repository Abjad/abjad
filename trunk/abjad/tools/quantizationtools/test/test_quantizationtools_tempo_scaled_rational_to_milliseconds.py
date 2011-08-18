from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.quantizationtools import tempo_scaled_rational_to_milliseconds


def test_quantizationtools_tempo_scaled_rational_to_milliseconds_01():
    beat = Fraction(1, 4)
    tempo = TempoMark((1, 4), 60)
    assert tempo_scaled_rational_to_milliseconds(beat, tempo) == 1000


def test_quantizationtools_tempo_scaled_rational_to_milliseconds_02():
    beat = Fraction(1, 4)
    tempo = TempoMark((1, 4), 55)
    assert tempo_scaled_rational_to_milliseconds(beat, tempo) == Fraction(60, 55) * 1000


def test_quantizationtools_tempo_scaled_rational_to_milliseconds_03():
    beat = Fraction(3, 4)
    tempo = TempoMark((1, 4), 60)
    assert tempo_scaled_rational_to_milliseconds(beat, tempo) == 3000
