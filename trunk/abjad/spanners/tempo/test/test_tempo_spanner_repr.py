from abjad import *


def test_tempo_spanner_repr_01( ):
   '''Tempo spanner repr gives tempo equation when possible.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   tempo_spanner = TempoSpanner(
      t[:], tempotools.TempoIndication(Rational(1, 8), 58))

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

   assert tempo_spanner.__repr__( ) == "TempoSpanner(8=58, c'8, d'8, e'8, f'8)"


def test_tempo_spanner_repr_02( ):
   '''Tempo spanner repr gives no equation when no 
   tempo indication is available.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   tempo_spanner = TempoSpanner(
      t[:], tempotools.TempoIndication(Rational(1, 8), 58))
   tempo_spanner.tempo_indication = None

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
   }
   '''
   
   assert tempo_spanner.__repr__( ) == "TempoSpanner(c'8, d'8, e'8, f'8)"
