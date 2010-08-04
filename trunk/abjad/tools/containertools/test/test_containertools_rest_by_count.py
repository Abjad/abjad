from abjad import *


def test_containertools_rest_by_count_01( ):
   '''Rest different parts of a container of length 9.'''

   ## Rest the lefthand part of the container

   t = RigidMeasure((9, 8), macros.scale(9))
   t = containertools.rest_by_count(t, 5, 'left', direction = 'automatic')
   assert componenttools.is_well_formed_component(t)
   assert str(t) == "|9/8, r8, r2, a'8, b'8, c''8, d''8|"

   t = RigidMeasure((9, 8), macros.scale(9))
   t = containertools.rest_by_count(t, 5, 'left', direction = 'big-endian')
   assert componenttools.is_well_formed_component(t)
   assert str(t) == "|9/8, r2, r8, a'8, b'8, c''8, d''8|"

   t = RigidMeasure((9, 8), macros.scale(9))
   t = containertools.rest_by_count(t, 5, 'left', direction = 'little-endian')
   assert componenttools.is_well_formed_component(t)
   assert str(t) == "|9/8, r8, r2, a'8, b'8, c''8, d''8|"

   ## Rest the righthand part of the container

   t = RigidMeasure((9, 8), macros.scale(9))
   t = containertools.rest_by_count(t, 4, 'right', direction = 'automatic')
   assert componenttools.is_well_formed_component(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, r2, r8|"

   t = RigidMeasure((9, 8), macros.scale(9))
   t = containertools.rest_by_count(t, 4, 'right', direction = 'big-endian')
   assert componenttools.is_well_formed_component(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, r2, r8|"

   t = RigidMeasure((9, 8), macros.scale(9))
   t = containertools.rest_by_count(t, 4, 'right', direction = 'little-endian')
   assert componenttools.is_well_formed_component(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, r8, r2|"


def test_containertools_rest_by_count_02( ):
   '''Glom leftmost two 1/8th notes, then turn into rest.'''

   t = RigidMeasure((5, 8), macros.scale(5))
   DuratedComplexBeam(t)
   containertools.rest_by_count(t, 2, 'left')

   r'''
   {
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
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 5/8\n\tr4\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #1\n\te'8 [\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #1\n\tf'8\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #0\n\tg'8 ]\n}"


def test_containertools_rest_by_count_03( ):
   '''Glom rightmost five - two = three 1/8th notes, 
      then turn into rest.'''

   t = RigidMeasure((5, 8), macros.scale(5))
   DuratedComplexBeam(t)
   containertools.rest_by_count(t, 2, 'right')

   r'''
   {
           \time 5/8
           \set stemLeftBeamCount = #0
           \set stemRightBeamCount = #1
           c'8 [
           \set stemLeftBeamCount = #1
           \set stemRightBeamCount = #1
           d'8 ]
           r4.
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 5/8\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #1\n\tc'8 [\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #1\n\td'8 ]\n\tr4.\n}"
