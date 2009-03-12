from abjad.helpers.in_terms_of import _in_terms_of


## TODO: Write tests.

def _measure_set_denominator(measure, denominator):
   from abjad.measure.base import _Measure
   if isinstance(measure, _Measure):
      old_meter = measure.meter.effective
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = _in_terms_of(old_meter_pair, denominator)
      measure.meter = new_meter
