from abjad import *


def test_measure_rest_by_count_01( ):
   '''Glom leftmost two 1/8th notes, then turn into rest.'''

   t = RigidMeasure((5, 8), scale(5))
   ComplexBeam(t)
   measure_rest_by_count(t, 2, rest = 'left')

   r'''
      \time 5/8
      r4
      \set stemLeftBeamCount = #1
      \set stemRightBeamCount = #1
      e'8 [
      \set stemLeftBeamCount = #1
      \set stemRightBeamCount = #1
      f'8
      \set stemLeftBeamCount = #1
      \set stemRightBeamCount = #0
      g'8 ]
   '''

   assert check(t)
   assert t.format == "\t\\time 5/8\n\tr4\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #1\n\te'8 [\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #1\n\tf'8\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #0\n\tg'8 ]"



def test_measure_rest_by_count_02( ):
   '''Glom rightmost five - two = three 1/8th notes, 
      then turn into rest.'''

   t = RigidMeasure((5, 8), scale(5))
   ComplexBeam(t)
   measure_rest_by_count(t, 2, rest = 'right')

   r'''
      \time 5/8
      \set stemLeftBeamCount = #0
      \set stemRightBeamCount = #1
      c'8 [
      \set stemLeftBeamCount = #1
      \set stemRightBeamCount = #1
      d'8 ]
      r4.
   '''

   assert check(t)
   assert t.format == "\t\\time 5/8\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #1\n\tc'8 [\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #1\n\td'8 ]\n\tr4."
