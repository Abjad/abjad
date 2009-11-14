from abjad import *


def test_tempotools_TempoIndication___sub__01( ):

   tempo_indication_1 = tempotools.TempoIndication(Rational(1, 4), 60)
   tempo_indication_2 = tempotools.TempoIndication(Rational(1, 4), 90)

   result = tempo_indication_1 - tempo_indication_2
   assert result == tempotools.TempoIndication(Rational(1, 4), -30)

   result = tempo_indication_2 - tempo_indication_1
   assert result == tempotools.TempoIndication(Rational(1, 4), 30)


def test_tempotools_TempoIndication___sub___01( ):

   tempo_indication_1 = tempotools.TempoIndication(Rational(1, 8), 42)
   tempo_indication_2 = tempotools.TempoIndication(Rational(1, 4), 90)

   result = tempo_indication_1 - tempo_indication_2
   assert result == tempotools.TempoIndication(Rational(1, 4), -6)

   result = tempo_indication_2 - tempo_indication_1
   assert result == tempotools.TempoIndication(Rational(1, 4), 6)
