from abjad import *


def test_tempotools_TempoIndication_maelzel_01( ):
   '''Maelzel metronome marking with integer-valued mark.'''

   t = tempotools.TempoIndication(Rational(3, 32), 52)
   assert t.maelzel == Rational(416, 3)

   
def test_tempotools_TempoIndication_maelzel_02( ):
   '''Maelzel metronome marking with float-valued mark.'''

   t = tempotools.TempoIndication(Rational(3, 32), 52.5)
   assert t.maelzel == 140.0
