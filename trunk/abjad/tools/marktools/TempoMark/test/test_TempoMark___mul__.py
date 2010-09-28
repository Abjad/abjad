from abjad import *


def test_TempoMark___mul___01( ):

   tempo_indication = marktools.TempoMark(Fraction(1, 4), 60)
   result = tempo_indication * Fraction(1, 2)
   assert result == marktools.TempoMark(Fraction(1, 4), 30)

   result = tempo_indication * Fraction(2, 3)
   assert result == marktools.TempoMark(Fraction(1, 4), 40)

   result = tempo_indication * Fraction(3, 4)
   assert result == marktools.TempoMark(Fraction(1, 4), 45)

   result = tempo_indication * Fraction(4, 5)
   assert result == marktools.TempoMark(Fraction(1, 4), 48)

   result = tempo_indication * Fraction(5, 6)
   assert result == marktools.TempoMark(Fraction(1, 4), 50)

   result = tempo_indication * Fraction(6, 7)
   assert result == marktools.TempoMark(
      Fraction(1, 4), Fraction(360, 7))


def test_TempoMark___mul___02( ):

   tempo_indication = marktools.TempoMark(Fraction(1, 4), 60)
   result = tempo_indication * 1
   assert result == marktools.TempoMark(Fraction(1, 4), 60)

   result = tempo_indication * 2
   assert result == marktools.TempoMark(Fraction(1, 4), 120)

   result = tempo_indication * 3
   assert result == marktools.TempoMark(Fraction(1, 4), 180)

   result = tempo_indication * 4
   assert result == marktools.TempoMark(Fraction(1, 4), 240)
