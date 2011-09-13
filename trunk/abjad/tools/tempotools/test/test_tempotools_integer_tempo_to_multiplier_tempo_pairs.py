from abjad import *
from abjad.tools import tempotools


def test_tempotools_integer_tempo_to_multiplier_tempo_pairs_01():

    pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(58, 8, 8)

    assert pairs == [(Fraction(1, 2), Fraction(29, 1)),
        (Fraction(1, 1), Fraction(58, 1)),
        (Fraction(3, 2), Fraction(87, 1)),
        (Fraction(2, 1), Fraction(116, 1))]


def test_tempotools_integer_tempo_to_multiplier_tempo_pairs_02():

    pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(58, 30, 30)

    assert pairs == [(Fraction(1, 2), Fraction(29, 1)),
        (Fraction(15, 29), Fraction(30, 1)),
        (Fraction(16, 29), Fraction(32, 1)),
        (Fraction(17, 29), Fraction(34, 1)),
        (Fraction(18, 29), Fraction(36, 1)),
        (Fraction(19, 29), Fraction(38, 1)),
        (Fraction(20, 29), Fraction(40, 1)),
        (Fraction(21, 29), Fraction(42, 1)),
        (Fraction(22, 29), Fraction(44, 1)),
        (Fraction(23, 29), Fraction(46, 1)),
        (Fraction(24, 29), Fraction(48, 1)),
        (Fraction(25, 29), Fraction(50, 1)),
        (Fraction(26, 29), Fraction(52, 1)),
        (Fraction(27, 29), Fraction(54, 1)),
        (Fraction(28, 29), Fraction(56, 1)),
        (Fraction(1, 1), Fraction(58, 1)),
        (Fraction(30, 29), Fraction(60, 1)),
        (Fraction(3, 2), Fraction(87, 1)),
        (Fraction(2, 1), Fraction(116, 1))]


def test_tempotools_integer_tempo_to_multiplier_tempo_pairs_03():

    pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(52, 4, 4)

    assert pairs == [(Fraction(1, 2), Fraction(26, 1)),
        (Fraction(3, 4), Fraction(39, 1)),
        (Fraction(1, 1), Fraction(52, 1)),
        (Fraction(3, 2), Fraction(78, 1)),
        (Fraction(2, 1), Fraction(104, 1))]


def test_tempotools_integer_tempo_to_multiplier_tempo_pairs_04():

    pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(52, 8, 8)

    assert pairs == [(Fraction(1, 2), Fraction(26, 1)),
        (Fraction(3, 4), Fraction(39, 1)),
        (Fraction(1, 1), Fraction(52, 1)),
        (Fraction(5, 4), Fraction(65, 1)),
        (Fraction(3, 2), Fraction(78, 1)),
        (Fraction(7, 4), Fraction(91, 1)),
        (Fraction(2, 1), Fraction(104, 1))]
