from abjad import *


def test_integer_tempo_to_multiplier_tempo_pairs_01( ):

   pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(58, 8, 8)

   assert pairs == [(Rational(1, 2), Rational(29, 1)),
       (Rational(1, 1), Rational(58, 1)),
       (Rational(3, 2), Rational(87, 1)),
       (Rational(2, 1), Rational(116, 1))]


def test_integer_tempo_to_multiplier_tempo_pairs_02( ):

   pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(58, 30, 30)

   assert pairs == [(Rational(1, 2), Rational(29, 1)),
       (Rational(15, 29), Rational(30, 1)),
       (Rational(16, 29), Rational(32, 1)),
       (Rational(17, 29), Rational(34, 1)),
       (Rational(18, 29), Rational(36, 1)),
       (Rational(19, 29), Rational(38, 1)),
       (Rational(20, 29), Rational(40, 1)),
       (Rational(21, 29), Rational(42, 1)),
       (Rational(22, 29), Rational(44, 1)),
       (Rational(23, 29), Rational(46, 1)),
       (Rational(24, 29), Rational(48, 1)),
       (Rational(25, 29), Rational(50, 1)),
       (Rational(26, 29), Rational(52, 1)),
       (Rational(27, 29), Rational(54, 1)),
       (Rational(28, 29), Rational(56, 1)),
       (Rational(1, 1), Rational(58, 1)),
       (Rational(30, 29), Rational(60, 1)),
       (Rational(3, 2), Rational(87, 1)),
       (Rational(2, 1), Rational(116, 1))]


def test_integer_tempo_to_multiplier_tempo_pairs_03( ):

   pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(52, 4, 4)

   assert pairs == [(Rational(1, 2), Rational(26, 1)),
       (Rational(3, 4), Rational(39, 1)),
       (Rational(1, 1), Rational(52, 1)),
       (Rational(3, 2), Rational(78, 1)),
       (Rational(2, 1), Rational(104, 1))]


def test_integer_tempo_to_multiplier_tempo_pairs_04( ):

   pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(52, 8, 8)

   assert pairs == [(Rational(1, 2), Rational(26, 1)),
       (Rational(3, 4), Rational(39, 1)),
       (Rational(1, 1), Rational(52, 1)),
       (Rational(5, 4), Rational(65, 1)),
       (Rational(3, 2), Rational(78, 1)),
       (Rational(7, 4), Rational(91, 1)),
       (Rational(2, 1), Rational(104, 1))]
