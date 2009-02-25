from abjad.helpers.make_best_meter import _make_best_meter
from abjad import *


def test_make_best_meter_01( ):
   '''Find only feasible denominator in denominators list.'''

   t = _make_best_meter(Rational(3, 2), [5, 6, 7, 8, 9])
   assert t == Meter(9, 6)


def test_make_best_meter_02( ):
   '''Use least feasible denominator in denominators list.'''

   t = _make_best_meter(Rational(3, 2), [4, 8, 16, 32])
   assert t == Meter(6, 4)


def test_make_best_meter_03( ):
   '''Make meter literally from duration.'''

   t = _make_best_meter(Rational(3, 2))
   assert t == Meter(3, 2)


def test_make_best_meter_04( ):
   '''Make meter literally from duration 
      because no feasible denomiantors in denominators list.'''

   t = _make_best_meter(Rational(3, 2), [7, 11, 13, 19])
   assert t == Meter(3, 2)
