from abjad import *


def test_tempo_indication_01( ):
   '''Tempo indication with integer-valued mark.'''

   t = TempoIndication(Rational(3, 32), 52)
   assert t.format == '\\tempo 16.=52'

   
def test_tempo_indication_02( ):
   '''Tempo indication with float-valued mark.'''

   t = TempoIndication(Rational(3, 32), 52.5)
   assert t.format == '\\tempo 16.=52.5'
