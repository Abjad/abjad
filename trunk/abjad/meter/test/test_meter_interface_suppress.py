from abjad import *
import py.test


def test_meter_interface_suppress_01( ):
   '''Suppress binary meter at format-time.'''

   t = RigidMeasure((7, 8), scale(7))
   t.meter.suppress = True

   r'''
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
        b'8
   '''

   assert t.format == "\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n\tb'8"


def test_meter_interface_suppress_02( ):
   '''Nonbinary meter suppression at format-time raises custom exception.'''

   t = RigidMeasure((8, 9), scale(8))
   t.meter.suppress = True

   assert py.test.raises(NonbinaryMeterSuppressionError, 't.format')
