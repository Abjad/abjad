from abjad import *


def test_tempo_spanner_01( ):
   '''Tempo spanner works on notes in voice.'''

   t = Voice(construct.scale(4))
   indication = TempoIndication(Rational(1, 8), 38)
   p = Tempo(t[:], indication)

   r'''\new Voice {
           \tempo 8=38
           c'8
           d'8
           e'8
           f'8
           %% tempo 8=38 ends here
   }'''

   assert check.wf(t)
   ## TODO: Make these two cases of effective tempo work ##
   #assert t[0].tempo.effective == TempoIndication(Rational(1, 8), 38)
   #assert t[1].tempo.effective == TempoIndication(Rational(1, 8), 38)
