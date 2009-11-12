from abjad import *


def test_durtools_in_terms_of_binary_multiple_01( ):

   duration = Rational(1, 2)
   assert durtools.in_terms_of_binary_multiple(duration, 2) == (1, 2)
   assert durtools.in_terms_of_binary_multiple(duration, 4) == (2, 4)
   assert durtools.in_terms_of_binary_multiple(duration, 8) == (4, 8)
   assert durtools.in_terms_of_binary_multiple(duration, 16) == (8, 16)


def test_durtools_in_terms_of_binary_multiple_02( ):

   duration = Rational(1, 2)
   assert durtools.in_terms_of_binary_multiple(duration, 3) == (3, 6)
   assert durtools.in_terms_of_binary_multiple(duration, 6) == (3, 6)
   assert durtools.in_terms_of_binary_multiple(duration, 12) == (6, 12)
   assert durtools.in_terms_of_binary_multiple(duration, 24) == (12, 24)


def test_durtools_in_terms_of_binary_multiple_03( ):

   duration = Rational(1, 2)
   assert durtools.in_terms_of_binary_multiple(duration, 5) == (5, 10)
   assert durtools.in_terms_of_binary_multiple(duration, 10) == (5, 10)
   assert durtools.in_terms_of_binary_multiple(duration, 20) == (10, 20)
   assert durtools.in_terms_of_binary_multiple(duration, 40) == (20, 40)
