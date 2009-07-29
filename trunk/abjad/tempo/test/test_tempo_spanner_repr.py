from abjad import *


def test_tempo_spanner_repr_01( ):
   '''Tempo spanner repr gives tempo equation when possible.'''

   t = Staff(construct.scale(4))
   tempo = Tempo(t[:], TempoIndication(Rational(1, 8), 58))

   r'''
   \new Staff {
           \tempo 8=58
           c'8
           d'8
           e'8
           f'8
           %% tempo 8=58 ends here
   }
   '''

   assert tempo.__repr__( ) == "Tempo(8=58, c'8, d'8, e'8, f'8)"


def test_tempo_spanner_repr_02( ):
   '''Tempo spanner repr gives no equation when no 
   tempo indication is available.'''

   t = Staff(construct.scale(4))
   tempo = Tempo(t[:], TempoIndication(Rational(1, 8), 58))
   tempo.indication = None

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
   }
   '''
   
   assert tempo.__repr__( ) == "Tempo(c'8, d'8, e'8, f'8)"
