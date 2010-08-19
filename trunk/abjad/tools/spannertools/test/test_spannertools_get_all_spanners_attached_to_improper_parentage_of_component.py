from abjad import *


def test_spannertools_get_all_spanners_attached_to_improper_parentage_of_component_01( ):

   staff = Staff(macros.scale(4))
   beam = spannertools.BeamSpanner(staff.leaves)
   slur = spannertools.SlurSpanner(staff.leaves)
   trill = spannertools.TrillSpanner(staff)

   r'''
   \new Staff {
      c'8 [ ( \startTrillSpan
      d'8
      e'8
      f'8 ] ) \stopTrillSpan
   }
   '''

   assert spannertools.get_all_spanners_attached_to_improper_parentage_of_component(staff[0]) == \
      set([beam, slur, trill])
   assert spannertools.get_all_spanners_attached_to_improper_parentage_of_component(staff) == \
      set([trill])
