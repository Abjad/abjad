from abjad import *


def test_metertools_make_binary_01( ):
   '''Make n/12 meters into n/8 meters, where possible.'''

   assert metertools.make_binary(Meter(1, 12)) == Meter(1, 12)
   assert metertools.make_binary(Meter(2, 12)) == Meter(2, 12)
   assert metertools.make_binary(Meter(3, 12)) == Meter(2, 8)
   assert metertools.make_binary(Meter(4, 12)) == Meter(4, 12)
   assert metertools.make_binary(Meter(5, 12)) == Meter(5, 12)
   assert metertools.make_binary(Meter(6, 12)) == Meter(4, 8)


def test_metertools_make_binary_02( ):
   '''Make n/14 meters into n/8 meters, where possible.'''

   assert metertools.make_binary(Meter(1, 14)) == Meter(1, 14)
   assert metertools.make_binary(Meter(2, 14)) == Meter(2, 14)
   assert metertools.make_binary(Meter(3, 14)) == Meter(3, 14)
   assert metertools.make_binary(Meter(4, 14)) == Meter(4, 14)
   assert metertools.make_binary(Meter(5, 14)) == Meter(5, 14)
   assert metertools.make_binary(Meter(6, 14)) == Meter(6, 14)
   assert metertools.make_binary(Meter(7, 14)) == Meter(4, 8)


def test_metertools_make_binary_03( ):
   '''Make n/24 meters into n/16 meters, where possible.'''

   assert metertools.make_binary(Meter(1, 24)) == Meter(1, 24)
   assert metertools.make_binary(Meter(2, 24)) == Meter(2, 24)
   assert metertools.make_binary(Meter(3, 24)) == Meter(2, 16)
   assert metertools.make_binary(Meter(4, 24)) == Meter(4, 24)
   assert metertools.make_binary(Meter(5, 24)) == Meter(5, 24)
   assert metertools.make_binary(Meter(6, 24)) == Meter(4, 16)
   assert metertools.make_binary(Meter(7, 24)) == Meter(7, 24)
   assert metertools.make_binary(Meter(8, 24)) == Meter(8, 24)


def test_metertools_make_binary_04( ):
   '''Make n/24 meters into n/8 meters, where possible.'''

   assert metertools.make_binary(Meter(1, 24), Rational(99)) == Meter(1, 24)
   assert metertools.make_binary(Meter(2, 24), Rational(99)) == Meter(2, 24)
   assert metertools.make_binary(Meter(3, 24), Rational(99)) == Meter(1, 8)
   assert metertools.make_binary(Meter(4, 24), Rational(99)) == Meter(4, 24)
   assert metertools.make_binary(Meter(5, 24), Rational(99)) == Meter(5, 24)
   assert metertools.make_binary(Meter(6, 24), Rational(99)) == Meter(2, 8)
   assert metertools.make_binary(Meter(7, 24), Rational(99)) == Meter(7, 24)
   assert metertools.make_binary(Meter(8, 24), Rational(99)) == Meter(8, 24)
