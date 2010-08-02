from abjad import *


def test_Meter___init____01( ):
   '''Meter can initialize from integer numerator and integer denominator.
   '''

   t = Meter(3, 8)

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Rational(3, 8)


def test_Meter___init____02( ):
   '''Meter can initialize from a numerator / denominator pair.
   '''

   t = Meter((3, 8))

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Rational(3, 8)


def test_Meter___init____03( ):
   '''Meter can initialize from a rational.
   '''

   t = Meter(Rational(3, 8))

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Rational(3, 8)


def test_Meter___init____04( ):
   '''Meter can initialize from another meter.
   '''

   t = Meter(Meter(3, 8))

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Rational(3, 8)
