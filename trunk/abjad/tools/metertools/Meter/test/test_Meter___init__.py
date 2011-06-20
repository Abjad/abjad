from abjad import *
from abjad.tools import metertools


def test_Meter___init___01( ):
   '''Meter can initialize from integer numerator and integer denominator.
   '''

   t = metertools.Meter(3, 8)

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Duration(3, 8)


def test_Meter___init___02( ):
   '''Meter can initialize from a numerator / denominator pair.
   '''

   t = metertools.Meter((3, 8))

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Duration(3, 8)


def test_Meter___init___03( ):
   '''Meter can initialize from a rational.
   '''

   t = metertools.Meter(Duration(3, 8))

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Duration(3, 8)


def test_Meter___init___04( ):
   '''Meter can initialize from another meter.
   '''

   t = metertools.Meter(metertools.Meter(3, 8))

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Duration(3, 8)
