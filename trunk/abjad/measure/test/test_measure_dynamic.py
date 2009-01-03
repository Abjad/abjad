from abjad import *
import py.test


def test_measure_dynamic_01( ):
   '''
   Dynamic measures determine meter on the fly.
   '''
  
   t = DynamicMeasure(scale(4))

   r'''
        \time 1/2
        c'8
        d'8
        e'8
        f'8
   '''

   assert t.format == "\t\\time 1/2\n\tc'8\n\td'8\n\te'8\n\tf'8"

   t.pop( )

   r'''
        \time 3/8
        c'8
        d'8
        e'8
   '''

   assert t.format == "\t\\time 3/8\n\tc'8\n\td'8\n\te'8"


def test_measure_dynamic_02( ):
   '''
   Dynamic measures block meter assignment.
   '''

   t = DynamicMeasure(scale(4))

   r'''
        \time 1/2
        c'8
        d'8
        e'8
        f'8
   '''

   assert py.test.raises(AttributeError, 't.meter = Meter(4, 8)')
