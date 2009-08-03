from abjad import *


def test_listtools_is_numeric_01( ):
   assert listtools.is_numeric([1, 2, 5.5, Rational(8, 3)])


def test_listtools_is_numeric_02( ):
   assert listtools.is_numeric([ ])


def test_listtools_is_numeric_03( ):
   assert not listtools.is_numeric([1, 2, Pitch(3)])
