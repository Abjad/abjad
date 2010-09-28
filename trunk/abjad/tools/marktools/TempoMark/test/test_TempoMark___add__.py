from abjad import *


def test_TempoMark___add___01( ):

   tempo_indication_1 = marktools.TempoMark(Fraction(1, 4), 60)
   tempo_indication_2 = marktools.TempoMark(Fraction(1, 4), 90)

   result = tempo_indication_1 + tempo_indication_2
   assert result == marktools.TempoMark(Fraction(1, 4), 150)

   result = tempo_indication_2 + tempo_indication_1
   assert result == marktools.TempoMark(Fraction(1, 4), 150)


def test_TempoMark___add___02( ):

   tempo_indication_1 = marktools.TempoMark(Fraction(1, 8), 42)
   tempo_indication_2 = marktools.TempoMark(Fraction(1, 4), 90)

   result = tempo_indication_1 + tempo_indication_2
   assert result == marktools.TempoMark(Fraction(1, 4), 174)

   result = tempo_indication_2 + tempo_indication_1
   assert result == marktools.TempoMark(Fraction(1, 4), 174)
