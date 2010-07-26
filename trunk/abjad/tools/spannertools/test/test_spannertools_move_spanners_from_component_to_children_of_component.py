from abjad import *


def test_spannertools_move_spanners_from_component_to_children_of_component_01( ):
   '''From parent to children.'''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)
   beam = Beam(t[:])

   r'''
   \new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }
   '''

   spannertools.move_spanners_from_component_to_children_of_component(t[0])

   assert t[0].spanners.attached == set([ ])
   assert t[0][0].spanners.attached == set([beam])
