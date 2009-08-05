from abjad.measure.measure import _Measure
from abjad.measure import RigidMeasure
from abjad.meter import Meter
from abjad.rational import Rational
from abjad.tools import check
from abjad.tools import containertools
from abjad.tools import metertools
from abjad.tools import parenttools
from abjad.tools.parenttools.switch import _switch
from abjad.tools.spannertools.give_dominant_to import _give_dominant_to


def measures_by_reference(measures):
   '''Measures in 'measures' may be strictly parent-contiguous.
      Or measures in 'measures' may all be outside-of-score.
      Measure fusion across intervening container boundaries is undefined.
      Calculate best new time signature and instantiate new measure.
      Give contents of 'measures' to new measure.
      Give dominant spanners of 'measures' to new measure.
      If parentage of in-score 'measures' to new measure.
      'Measures' end up empty, undominated and outside-of-score.'''

   check.assert_components(measures, 
      klasses = (_Measure), contiguity = 'strict', share = 'parent')

   if len(measures) == 0:
      return None

   ## TODO: Instantiate a new measure, even length is 1 ##

   if len(measures) == 1:
      return measures[0]

   parent, start, stop = parenttools.get_with_indices(measures)

   old_denominators = [ ]
   new_duration = Rational(0)
   for measure in measures:
      effective_meter = measure.meter.effective
      old_denominators.append(effective_meter.denominator)
      new_duration += effective_meter.duration

   new_meter = metertools.make_best(new_duration, old_denominators)

   music = [ ]
   for measure in measures:
      ## scale before reassignment to prevent tie chain scale drama
      multiplier = ~new_meter.multiplier * measure.meter.effective.multiplier
      containertools.contents_scale(measure, multiplier)
      measure_music = measure[:]
      _switch(measure_music, None)
      #containertools.contents_scale(measure_music, multiplier)
      music += measure_music

   new_measure = RigidMeasure(new_meter, music)

   if parent is not None:
      _give_dominant_to(measures, [new_measure])

   _switch(measures, None)
   if parent is not None:
      parent.insert(start, new_measure)

   return new_measure 
