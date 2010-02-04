from abjad import *


def test_durtools_duration_string_to_rational_01( ):

   assert durtools.duration_string_to_rational('8') == Rational(1, 8)
   assert durtools.duration_string_to_rational('8.') == Rational(3, 16)
   assert durtools.duration_string_to_rational('8..') == Rational(7, 32)
   assert durtools.duration_string_to_rational('8...') == Rational(15, 64)


def test_durtools_duration_string_to_rational_02( ):

   assert durtools.duration_string_to_rational(r'\breve') == Rational(2, 1)
   assert durtools.duration_string_to_rational(r'\breve.') == Rational(3, 1)
   assert durtools.duration_string_to_rational(r'\breve..') == Rational(7, 2)
   assert durtools.duration_string_to_rational(r'\breve...') == Rational(15, 4)
