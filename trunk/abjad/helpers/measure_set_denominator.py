from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.measure import _Measure


def measure_set_denominator(measure, denominator):
   '''Rewrite the denominator of the meter of 'measure'.
      Keep all contents of 'measure' unchanged.
      Return 'measure'.'''

   if isinstance(measure, _Measure):
      old_meter = measure.meter.effective
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = _in_terms_of(old_meter_pair, denominator)
      measure.meter = new_meter

   return measure
