from abjad import *
from abjad.tools import durtools


def test_durtools_rewrite_rational_under_new_tempo_01( ):

   tempo_indication_1 = contexttools.TempoMark(Fraction(1, 4), 60)
   tempo_indication_2 = contexttools.TempoMark(Fraction(1, 4), 90)
  
   result = durtools.rewrite_rational_under_new_tempo(
      Fraction(1, 8), tempo_indication_1, tempo_indication_2)
   assert result == Fraction(3, 16)

   result = durtools.rewrite_rational_under_new_tempo(
      Fraction(1, 12), tempo_indication_1, tempo_indication_2)
   assert result == Fraction(1, 8)

   result = durtools.rewrite_rational_under_new_tempo(
      Fraction(1, 16), tempo_indication_1, tempo_indication_2)
   assert result == Fraction(3, 32)

   result = durtools.rewrite_rational_under_new_tempo(
      Fraction(1, 24), tempo_indication_1, tempo_indication_2)
   assert result == Fraction(1, 16)
