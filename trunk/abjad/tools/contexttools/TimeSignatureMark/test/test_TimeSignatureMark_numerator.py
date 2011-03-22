from abjad import *


def test_TimeSignatureMark_numerator_01( ):
   '''Time signature numerator is read / write.
   '''

   meter = contexttools.TimeSignatureMark(3, 8)
   assert meter.numerator == 3

   meter.numerator = 4
   assert meter.numerator == 4
