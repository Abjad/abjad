from abjad.measure.measure import _Measure
from abjad.meter import Meter
from abjad.tools import durtools


def denominator_set(measure, denominator):
   '''Rewrite the denominator of the meter of 'measure'.
      Keep all contents of 'measure' unchanged.
      Return 'measure'.'''

   if isinstance(measure, _Measure):
      ## to allow iteration inside zero-update loop
      forced_meter = measure.meter.forced
      if forced_meter is not None:
         old_meter = forced_meter
      else:
         old_meter = measure.meter.effective
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = durtools.in_terms_of(old_meter_pair, denominator)
      measure.meter.forced = Meter(new_meter)

   return measure
