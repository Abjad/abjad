from abjad import *
import py.test


def test_DynamicMeasure_bequeath_01( ):
   '''Bequeath DynamicMeasure contents to RigidMeasure.'''

   t = DynamicMeasure(macros.scale(4))

   r'''
   {
           \time 1/2
           c'8
           d'8
           e'8
           f'8
   }
   '''

   u = RigidMeasure((4, 8), [ ])
   containertools.move_parentage_children_and_spanners_from_components_to_empty_container([t], u)

   r'''
   {
           \time 4/8
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert u.format == "{\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
   assert t.format == '{\n\t\\time 0/1\n}'
