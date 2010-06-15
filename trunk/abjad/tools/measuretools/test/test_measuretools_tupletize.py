from abjad import *


def test_measuretools_tupletize_01( ):
   '''Tupletize one measure, supplement one note.'''

   t = RigidMeasure((4, 8), leaftools.make_repeated_notes(4))
   measuretools.tupletize(t, leaftools.make_repeated_notes(1))

   r'''
   {
           \time 4/8
           \times 4/5 {
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 4/8\n\t\\times 4/5 {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n}"


def test_measuretools_tupletize_02( ):
   '''Tupletize one measure, supplement one rest.'''

   t = RigidMeasure((4, 8), leaftools.make_repeated_notes(4))
   measuretools.tupletize(t, [Rest((1, 4))])

   r'''
   {
           \time 4/8
           \times 2/3 {
                   c'8
                   c'8
                   c'8
                   c'8
                   r4
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 4/8\n\t\\times 2/3 {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tr4\n\t}\n}"
