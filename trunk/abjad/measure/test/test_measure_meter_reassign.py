from abjad import *


def test_measure_meter_reassign_01( ):
   '''
   Measures allow meter reassignment.
   '''

   t = Measure((4, 8), scale(4))

   r'''
        \time 4/8
        c'8
        d'8
        e'8
        f'8
   '''

   t.pop( )
   t.meter = Meter(3, 8)

   r'''
        \time 3/8
        c'8
        d'8
        e'8
   '''

   assert t.format == "\t\\time 3/8\n\tc'8\n\td'8\n\te'8"
