from abjad import *


def test_tempo_indication_01( ):
   '''Tempo indication with integer-valued mark.'''

   t = TempoIndication(Rational(3, 32), 52)
   assert t.format == '\\tempo 16.=52'

   
def test_tempo_indication_02( ):
   '''Tempo indication with float-valued mark.'''

   t = TempoIndication(Rational(3, 32), 52.5)
   assert t.format == '\\tempo 16.=52.5'


def test_tempo_indication_03( ):
   '''Tempo indications compare equal when duration and mark match.'''
   
   t1 = TempoIndication(Rational(3, 32), 52)
   t2 = TempoIndication(Rational(3, 32), 52)
   assert t1 == t2
   

def test_tempo_indication_04( ):
   '''Tempo indications do not compare equal
      when mathematically equal.'''
   
   t1 = TempoIndication(Rational(3, 32), 52)
   t2 = TempoIndication(Rational(6, 32), 104)
   assert not t1 == t2
