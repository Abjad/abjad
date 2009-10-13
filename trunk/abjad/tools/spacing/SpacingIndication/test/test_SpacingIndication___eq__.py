from abjad import *


def test_spacing_indication_eq_01( ):
   '''Spacing indications compare equal when 
      normalized spacing durations compare equal.'''

   tempo_indication = tempotools.TempoIndication(Rational(1, 8), 38)
   p = spacing.SpacingIndication(tempo_indication, Rational(1, 68))
   
   tempo_indication = tempotools.TempoIndication(Rational(1, 4), 76)
   q = spacing.SpacingIndication(tempo_indication, Rational(1, 68))

   assert p == q
   

def test_spacing_indication_eq_02( ):
   '''Spacing indications compare not equal when 
      normalized spacing durations compare not equal.'''

   tempo_indication = tempotools.TempoIndication(Rational(1, 8), 38)
   p = spacing.SpacingIndication(tempo_indication, Rational(1, 68))
   
   tempo_indication = tempotools.TempoIndication(Rational(1, 8), 38)
   q = spacing.SpacingIndication(tempo_indication, Rational(1, 78))

   assert p != q
