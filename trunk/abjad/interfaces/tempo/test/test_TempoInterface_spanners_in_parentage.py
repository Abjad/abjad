from abjad import *


def test_TempoInterface_spanners_in_parentage_01( ):
   '''Return unordered set of all spanners attaching to 
   any component in the parentage of client, including client.
   '''

   t = Staff(macros.scale(4))
   tempo_indication = tempotools.TempoIndication(Rational(1, 4), 60)
   tempo_spanner = TempoSpanner(t, tempo_indication)

   r'''
   \new Staff {
           \tempo 4=60
           c'8
           d'8
           e'8
           f'8
           %% tempo 4=60 ends here
   }
   '''

   spanners_in_parentage = t.leaves[0].tempo.spanners_in_parentage

   assert isinstance(spanners_in_parentage, set)
   assert len(spanners_in_parentage) == 1
   assert tempo_spanner in spanners_in_parentage
