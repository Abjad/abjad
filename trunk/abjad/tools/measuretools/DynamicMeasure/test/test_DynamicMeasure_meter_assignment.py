from abjad import *
import py.test


def test_DynamicMeasure_meter_assignment_01( ):
   '''Dynamic measures block meter assignment.
   '''
   py.test.skip('fix and decide how to model dynamic measure attachment errors.')

   t = measuretools.DynamicMeasure(macros.scale(4))

   r'''
   \time 1/2
        c'8
        d'8
        e'8
        f'8
   '''

   ## author asserts here ##
