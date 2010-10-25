from abjad import *


def test_listtools_all_are_numbers_01( ):
   '''True when all elements in sequence are numbers.
   '''

   assert listtools.all_are_numbers([1, 2, 5.5, Fraction(8, 3)])


def test_listtools_all_are_numbers_02( ):
   '''True on empty sequence.
   '''

   assert listtools.all_are_numbers([ ])


def test_listtools_all_are_numbers_03( ):
   '''False otherwise.
   '''

   assert not listtools.all_are_numbers([1, 2, pitchtools.NamedChromaticPitch(3)])
