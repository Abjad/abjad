from abjad import *
import py.test


def test_durtools_to_clock_string_01( ):
   
   assert durtools.to_clock_string(1.5) == "1'30''"
   assert durtools.to_clock_string(1.13) == "1'08''"
   assert durtools.to_clock_string(0.333) == "0'20''"
   assert durtools.to_clock_string(2.70) == "2'42''"
   assert durtools.to_clock_string(4) == "4'00''"
   assert durtools.to_clock_string(4.08) == "4'05''"


def test_durtools_to_clock_string_02( ):

   assert durtools.to_clock_string(Rational(27, 16)) == "1'41''"
   assert durtools.to_clock_string(Rational(28, 16)) == "1'45''"
   assert durtools.to_clock_string(Rational(29, 16)) == "1'49''"
   assert durtools.to_clock_string(Rational(3, 2)) == "1'30''"
   assert durtools.to_clock_string(Rational(5, 6)) == "0'50''"
   assert durtools.to_clock_string(Rational(1, 20)) == "0'03''"


def test_durtools_to_clock_string_03( ):

   assert py.test.raises(ValueError, 'durtools.to_clock_string(-1.5)')

