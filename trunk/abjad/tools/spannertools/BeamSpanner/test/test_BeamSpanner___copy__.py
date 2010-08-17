from abjad import *


def test_BeamSpanner___copy___01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[:4])
   u = componenttools.clone_components_and_fracture_crossing_spanners(t[:1])[0]
   len(u.spanners.attached) == 1
   assert u.beam.spanned and u.beam.only


def test_BeamSpanner___copy___02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[:4])
   u = componenttools.clone_components_and_immediate_parent_of_first_component(t[0 : 1])
   assert u[0].beam.spanned and u[0].beam.only


def test_BeamSpanner___copy___03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[:4])
   u = componenttools.clone_components_and_immediate_parent_of_first_component(t[0:2])
   assert u[0].beam.spanned and u[0].beam.first
   assert u[1].beam.spanned and u[1].beam.last
   

def test_BeamSpanner___copy___04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[:4])
   u = componenttools.clone_components_and_immediate_parent_of_first_component(t[0:4])
   assert u[0].beam.spanned and u[0].beam.first
   assert u[1].beam.spanned
   assert u[2].beam.spanned
   assert u[3].beam.spanned and u[3].beam.last
