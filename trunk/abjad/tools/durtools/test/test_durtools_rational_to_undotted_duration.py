from abjad import *


def test_durtools_rational_to_undotted_duration_01( ):

   result = durtools.rational_to_undotted_duration(Rational(5, 16))
   assert result == Rational(4, 16)

   result = durtools.rational_to_undotted_duration(Rational(6, 16))
   assert result == Rational(4, 16)

   result = durtools.rational_to_undotted_duration(Rational(7, 16))
   assert result == Rational(4, 16)

   result = durtools.rational_to_undotted_duration(Rational(8, 16))
   assert result == Rational(8, 16)


def test_durtools_rational_to_undotted_duration_02( ):

   result = durtools.rational_to_undotted_duration(Rational(1, 1))
   assert result == Rational(1, 1)

   result = durtools.rational_to_undotted_duration(Rational(2, 1))
   assert result == Rational(2, 1)

   result = durtools.rational_to_undotted_duration(Rational(4, 1))
   assert result == Rational(4, 1)

   result = durtools.rational_to_undotted_duration(Rational(8, 1))
   assert result == Rational(8, 1)
