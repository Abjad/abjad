from abjad import *


def test_tempotools_TempoIndication___eq___01( ):
   '''Tempo indications compare equal when duration and mark match.'''
   
   t1 = tempotools.TempoIndication(Rational(3, 32), 52)
   t2 = tempotools.TempoIndication(Rational(3, 32), 52)
   assert t1 == t2
   

def test_tempotools_TempoIndication___eq___02( ):
   '''Tempo indications do not compare equal
   when mathematically equal.
   '''
   
   t1 = tempotools.TempoIndication(Rational(3, 32), 52)
   t2 = tempotools.TempoIndication(Rational(6, 32), 104)
   assert not t1 == t2
