from abjad import *


def test_rigid_measure_meter_assignment_01( ):
   '''RigidMeasures allow meter reassignment.'''

   t = RigidMeasure((4, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))

   r'''
   {
           \time 4/8
           c'8
           d'8
           e'8
           f'8
   }
   '''

   t.pop( )
   t.meter.forced = Meter(3, 8)

   r'''
   {
           \time 3/8
           c'8
           d'8
           e'8
   }
   '''

   assert t.format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"
