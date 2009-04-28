from abjad import *
import py.test


def test_iterate_measure_next_01( ):
   
   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   Container(t[:2])
   pitchtools.diatonicize(t)

   r'''\new Staff {
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
   }'''

   assert iterate.measure_next(t) is t[0][0]
   assert iterate.measure_next(t[0]) is t[0][0]
   assert iterate.measure_next(t[0][0]) is t[0][1]
   assert iterate.measure_next(t[0][1]) is t[1]
   assert iterate.measure_next(t[1]) is t[2]
   #assert py.test.raises(StopIteration, 'iterate.measure_next(t[2])')
   assert iterate.measure_next(t[2]) is None
   assert iterate.measure_next(t.leaves[0]) is t[0][0]
   assert iterate.measure_next(t.leaves[1]) is t[0][0]
   assert iterate.measure_next(t.leaves[2]) is t[0][1]
   assert iterate.measure_next(t.leaves[3]) is t[0][1]
   assert iterate.measure_next(t.leaves[4]) is t[1]
   assert iterate.measure_next(t.leaves[5]) is t[1]
   assert iterate.measure_next(t.leaves[6]) is t[2]
   assert iterate.measure_next(t.leaves[7]) is t[2]
