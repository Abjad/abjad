from abjad import *


def test_TempoIndication___init___01( ):
   '''Init tempo indication with integer-valued mark.'''

   t = tempotools.TempoIndication(Rational(3, 32), 52)
   assert t.format == '\\tempo 16.=52'

   
def test_TempoIndication___init___02( ):
   '''Init tempo indication with float-valued mark.'''

   t = tempotools.TempoIndication(Rational(3, 32), 52.5)
   assert t.format == '\\tempo 16.=52.5'


def test_TempoIndication___init___03( ):
   '''Init tempo indication from tempo indication.'''

   t = tempotools.TempoIndication(Rational(3, 32), 52)
   new = tempotools.TempoIndication(t)

   assert t == new
   assert t is not new

   assert t.duration == new.duration
   assert t.duration is not new.duration
