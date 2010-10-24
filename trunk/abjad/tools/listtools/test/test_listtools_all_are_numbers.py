from abjad import *


def test_listtools_all_are_numbers_01( ):
   assert listtools.all_are_numbers([1, 2, 5.5, Fraction(8, 3)])


def test_listtools_all_are_numbers_02( ):
   assert listtools.all_are_numbers([ ])


def test_listtools_all_are_numbers_03( ):
   assert not listtools.all_are_numbers([1, 2, pitchtools.NamedChromaticPitch(3)])
