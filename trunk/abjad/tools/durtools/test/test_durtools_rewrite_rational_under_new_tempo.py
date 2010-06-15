from abjad import *


def test_durtools_rewrite_rational_under_new_tempo_01( ):

   tempo_indication_1 = tempotools.TempoIndication(Rational(1, 4), 60)
   tempo_indication_2 = tempotools.TempoIndication(Rational(1, 4), 90)
  
   result = durtools.rewrite_rational_under_new_tempo(
      Rational(1, 8), tempo_indication_1, tempo_indication_2)
   assert result == Rational(3, 16)

   result = durtools.rewrite_rational_under_new_tempo(
      Rational(1, 12), tempo_indication_1, tempo_indication_2)
   assert result == Rational(1, 8)

   result = durtools.rewrite_rational_under_new_tempo(
      Rational(1, 16), tempo_indication_1, tempo_indication_2)
   assert result == Rational(3, 32)

   result = durtools.rewrite_rational_under_new_tempo(
      Rational(1, 24), tempo_indication_1, tempo_indication_2)
   assert result == Rational(1, 16)
