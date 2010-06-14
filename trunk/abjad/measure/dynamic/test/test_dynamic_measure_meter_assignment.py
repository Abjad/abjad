from abjad import *
import py.test


def test_dynamic_measure_meter_assignment_01( ):
   '''Dynamic measures block meter assignment.'''

   t = DynamicMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))

   r'''
   \time 1/2
        c'8
        d'8
        e'8
        f'8'''

   assert py.test.raises(MeterAssignmentError, 't.meter.forced = Meter(4, 8)')
