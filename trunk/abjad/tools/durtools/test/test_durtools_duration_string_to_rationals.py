from abjad import *


def test_durtools_duration_string_to_rationals_01( ):

   duration_string = '8.. 32 8.. 32'
   rationals = durtools.duration_string_to_rationals(duration_string)

   assert rationals == [
      Rational(7, 32), Rational(1, 32), Rational(7, 32), Rational(1, 32)]
