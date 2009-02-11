from abjad.helpers.iterate import iterate
from abjad.rational.rational import Rational
from abjad.tuplet.tuplet import _Tuplet


def measures_subsume(expr):
   '''Subsume all measures in expr containing top-level tuplet;
      measures usually become nonbinary as as result of subsumption.'''

   for measure in iterate(expr, '_Measure'): 
      if len(measure) == 1:
         if isinstance(measure[0], _Tuplet):
            tuplet = measure[0]
            tuplet_multiplier = tuplet.duration.multiplier
            tuplet_denominator = tuplet_multiplier._d
            meter = measure.meter.effective
            meter_rational = Rational(meter.numerator, meter.denominator)
            numerator = meter_rational._n * tuplet_denominator
            denominator = meter_rational._d * tuplet_denominator
            measure.meter = (numerator, denominator)
            meter_multiplier = measure.meter.effective.multiplier
            written_adjustment = tuplet_multiplier / meter_multiplier
            measure[:] = tuplet[:]
            for leaf in measure.leaves:
               new_written_duration = written_adjustment * leaf.duration.written
               leaf.duration.written = new_written_duration
