from abjad import *
from abjad.tools import metertools
import py.test


def test_Meter_duration_01( ):
   '''
   Meters implement a read-only duration.
   '''

   t = metertools.Meter(3, 8)

   assert t.duration == Duration(3, 8)
   assert py.test.raises(AttributeError, 't.duration = (5, 16)')


def test_Meter_duration_02( ):
   '''
   Meters implement read-only duration.
   '''

   t = metertools.Meter(6, 16)

   assert t.duration == Duration(3, 8)
   assert py.test.raises(AttributeError, 't.duration = (5, 16)')
