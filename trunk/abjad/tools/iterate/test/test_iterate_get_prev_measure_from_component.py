from abjad import *
import py.test


def test_iterate_get_prev_measure_from_component_01( ):
   
   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 4)
   Container(t[:2])
   pitchtools.diatonicize(t)

   r'''
   \new Staff {
           {
                           \time 2/8
                           c'8
                           d'8
                           \time 2/8
                           e'8
                           f'8
           }
                   \time 2/8
                   g'8
                   a'8
                   \time 2/8
                   b'8
                   c''8
   }
   '''

   assert iterate.get_prev_measure_from_component(t) is t[-1]
   assert iterate.get_prev_measure_from_component(t[0]) is t[0][1]
   #assert py.test.raises(StopIteration, 'iterate.get_prev_measure_from_component(t[0][0])')
   assert iterate.get_prev_measure_from_component(t[0][0]) is None
   assert iterate.get_prev_measure_from_component(t[0][1]) is t[0][0]
   assert iterate.get_prev_measure_from_component(t[1]) is t[0][1]
   assert iterate.get_prev_measure_from_component(t[2]) is t[1]
   assert iterate.get_prev_measure_from_component(t.leaves[0]) is t[0][0]
   assert iterate.get_prev_measure_from_component(t.leaves[1]) is t[0][0]
   assert iterate.get_prev_measure_from_component(t.leaves[2]) is t[0][1]
   assert iterate.get_prev_measure_from_component(t.leaves[3]) is t[0][1]
   assert iterate.get_prev_measure_from_component(t.leaves[4]) is t[1]
   assert iterate.get_prev_measure_from_component(t.leaves[5]) is t[1]
   assert iterate.get_prev_measure_from_component(t.leaves[6]) is t[2]
   assert iterate.get_prev_measure_from_component(t.leaves[7]) is t[2]


def test_iterate_get_prev_measure_from_component_02( ):
   '''Can retrieve last measure in a Python list.'''

   t = [RigidMeasure((2, 8), macros.scale(2)), Note(0, (1, 4))]

   assert iterate.get_prev_measure_from_component(t) is t[0]
