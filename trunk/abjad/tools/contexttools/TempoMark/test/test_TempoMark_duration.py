from abjad import *


def test_TempoMark_duration_01( ):
   '''Duration of tempo mark is read / write.
   '''

   tempo = contexttools.TempoMark(Fraction(1, 8), 52)
   assert tempo.duration == Fraction(1, 8)

   tempo.duration = Fraction(1, 4)
   assert tempo.duration == Fraction(1, 4)
