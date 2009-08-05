from abjad import *


def test_tempo_indication_init_01( ):
   '''Init tempo indication with integer-valued mark.'''

   t = TempoIndication(Rational(3, 32), 52)
   assert t.format == '\\tempo 16.=52'

   
def test_tempo_indication_init_02( ):
   '''Init tempo indication with float-valued mark.'''

   t = TempoIndication(Rational(3, 32), 52.5)
   assert t.format == '\\tempo 16.=52.5'


def test_tempo_indication_init_03( ):
   '''Init tempo indication from tempo indication.'''

   t = TempoIndication(Rational(3, 32), 52)
   new = TempoIndication(t)

   assert t == new
   assert t is not new

   assert t.duration == new.duration
   assert t.duration is not new.duration
