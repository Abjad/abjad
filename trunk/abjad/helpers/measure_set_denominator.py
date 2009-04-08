from abjad.tools import mathtools
from abjad.measure.measure import _Measure
from abjad.meter.meter import Meter


def measure_set_denominator(measure, denominator):
   '''Rewrite the denominator of the meter of 'measure'.
      Keep all contents of 'measure' unchanged.
      Return 'measure'.'''

   if isinstance(measure, _Measure):
      old_meter = measure.meter.effective
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = mathtools.in_terms_of(old_meter_pair, denominator)
      measure.meter.forced = Meter(new_meter)

   return measure
