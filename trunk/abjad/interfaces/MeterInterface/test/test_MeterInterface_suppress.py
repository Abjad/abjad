from abjad import *
import py.test


def test_MeterInterface_suppress_01( ):
   '''Suppress binary meter at format-time.'''

   t = Measure((7, 8), macros.scale(7))
   #t.meter.suppress = True
   t.meter.effective.suppress = True

   r'''
   {
           c'8
           d'8
           e'8
           f'8
           g'8
           a'8
           b'8
   }
   '''

   assert t.format == "{\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n\tb'8\n}"


def test_MeterInterface_suppress_02( ):
   '''Nonbinary meter suppression at format-time raises custom exception.'''

   t = Measure((8, 9), macros.scale(8))
   #t.meter.suppress = True
   t.meter.effective.suppress = True

   assert py.test.raises(NonbinaryMeterSuppressionError, 't.format')
