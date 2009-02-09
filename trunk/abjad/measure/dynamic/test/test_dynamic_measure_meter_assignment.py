from abjad import *
import py.test


def test_dynamic_measure_meter_assignment_01( ):
   '''Dynamic measures block meter assignment.'''

   t = DynamicMeasure(scale(4))

   r'''
        \time 1/2
        c'8
        d'8
        e'8
        f'8
   '''

   assert py.test.raises(AttributeError, 't.meter = Meter(4, 8)')
