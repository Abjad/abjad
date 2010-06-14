from abjad import *


def test_spannertools_iterate_components_backward_01( ):

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8 [
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8 ]
           }
   }
   '''

   components = spannertools.iterate_components_backward(p)
   components = list(components)
   leaves = t.leaves

   assert components[0] is t[-1]
   assert components[1] is leaves[-1]
   assert components[2] is leaves[-2]
   assert components[3] is t[-2]
   assert components[4] is leaves[-3]
   assert components[5] is leaves[-4]
