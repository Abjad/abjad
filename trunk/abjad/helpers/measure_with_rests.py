from abjad.helpers.leaf_list import leaf_list
from abjad.measure.rigid.measure import RigidMeasure
from abjad.rest.rest import Rest


def measure_with_rests(meter_token):
   '''Return measure filled with one or more rests.

      abjad> measure_with_rests((9, 16))
      Measure(9/16, [r2, r16])'''   

   assert isinstance(meter_token, tuple)
   assert len(meter_token) == 2

   return RigidMeasure(meter_token, leaf_list(Rest, meter_token))
