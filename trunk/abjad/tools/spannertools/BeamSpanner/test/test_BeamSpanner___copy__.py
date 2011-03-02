from abjad import *


def test_BeamSpanner___copy___01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[:4])
   u = componenttools.clone_components_and_fracture_crossing_spanners(t[:1])[0]
   #len(u.spanners.attached) == 1
   len(u.spanners) == 1

   #assert u.beam.spanned and u.beam.only

   assert spannertools.get_beam_spanner_attached_to_component(u)._is_my_only_leaf(u)


def test_BeamSpanner___copy___02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[:4])
   u = componenttools.clone_components_and_immediate_parent_of_first_component(t[0:1])

   #assert u[0].beam.spanned and u[0].beam.only

   assert spannertools.get_beam_spanner_attached_to_component(u[0])._is_my_only_leaf(u[0])


def test_BeamSpanner___copy___03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[:4])
   u = componenttools.clone_components_and_immediate_parent_of_first_component(t[0:2])

   #assert u[0].beam.spanned and u[0].beam.first
   #assert u[1].beam.spanned and u[1].beam.last

   assert spannertools.get_beam_spanner_attached_to_component(u[0])._is_my_first_leaf(u[0])
   assert spannertools.get_beam_spanner_attached_to_component(u[1])._is_my_last_leaf(u[1])
   

def test_BeamSpanner___copy___04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[:4])
   u = componenttools.clone_components_and_immediate_parent_of_first_component(t[0:4])

   #assert u[0].beam.spanned and u[0].beam.first
   #assert u[1].beam.spanned
   #assert u[2].beam.spanned
   #assert u[3].beam.spanned and u[3].beam.last

   assert spannertools.get_beam_spanner_attached_to_component(u[0])._is_my_first_leaf(u[0])
   assert spannertools.is_component_with_beam_spanner_attached(u[1])
   assert spannertools.is_component_with_beam_spanner_attached(u[2])
   assert spannertools.get_beam_spanner_attached_to_component(u[3])._is_my_last_leaf(u[3])
