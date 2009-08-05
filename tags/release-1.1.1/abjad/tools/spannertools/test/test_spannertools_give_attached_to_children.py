from abjad import *


def test_spannertools_give_attached_to_children_01( ):
   '''From parent to children.'''

   t = Voice(Container(construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   beam = Beam(t[:])

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }'''

   spannertools.give_attached_to_children(t[0])

   assert t[0].spanners.attached == set([ ])
   assert t[0][0].spanners.attached == set([beam])
