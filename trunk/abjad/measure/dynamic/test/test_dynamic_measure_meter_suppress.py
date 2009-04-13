from abjad import *


def test_dynamic_measure_meter_suppress_01( ):
   '''It is possible to suppress meter from dynamic measures;
      set suppress on the meter interface.'''

   t = DynamicMeasure(construct.scale(4))
   t.meter.suppress = True

   r'''
      c'8
      d'8
      e'8
      f'8
   '''

   assert check.wf(t)
   assert t.format == "\tc'8\n\td'8\n\te'8\n\tf'8"
