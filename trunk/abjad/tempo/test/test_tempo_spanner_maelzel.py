from abjad import *
import py.test


def test_tempo_spanner_maelzel_01( ):
   '''Tempo spanner with tempo indication gives Maezel metronome marking.'''

   p = Tempo([ ], TempoIndication(Rational(1, 8), 48))
   assert p.maelzel == Rational(96, 1)


def test_tempo_spanner_maelzel_02( ):
   '''Tempo spanner without tempo indication raises exception.'''

   p = Tempo([ ])
   assert py.test.raises(UndefinedTempoError, 'p.maelzel')
