from abjad.tools import durtools
from abjad.tools import metertools
from abjad.tools.measuretools.scale import scale as measuretools_scale


## TODO: Implement measuretools.nonbinary_to_binary( ) ##

def binary_to_nonbinary(measure, new_denominator_factor):
   '''Make binary measure into equivalent nonbinary measure.
      New denominator factor like clever form of 1:
      3/3 or 5/5 or 7/7, etc.
      Prolated duration of measure exactly same before and after.
      Derive new measure multiplier and scale contents.
      Then pick best meter.
      This is a special case of scale_and_remeter.'''

   ## save old meter duration
   old_meter_duration = measure.meter.effective.duration

   ## find new meter
   new_meter = metertools.make_best(
      old_meter_duration, factor = new_denominator_factor)

   ## find new measure multiplier
   new_measure_multiplier = durtools.denominator_to_multiplier(
      new_denominator_factor) 

   ## inverse scale measure ... but throw away resultant meter
   measuretools_scale(measure, ~new_measure_multiplier)

   ## assign new meter
   measure.meter.forced = new_meter
