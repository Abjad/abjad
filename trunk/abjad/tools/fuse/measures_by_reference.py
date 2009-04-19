from abjad.measure.measure import _Measure
from abjad.measure.rigid.measure import RigidMeasure
from abjad.meter.meter import Meter
from abjad.rational.rational import Rational
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
      multiplier = ~new_meter.multiplier * measure.meter.effective.multiplier
      measure_music = measure[:]
      _switch(measure_music, None) # new
      containertools.contents_scale(measure_music, multiplier)
      music += measure_music

   #_switch(music, None)
   new_measure = RigidMeasure(new_meter, music)
   _switch(measures, None)
   if parent is not None:  # new
      parent.insert(start, new_measure)

   for measure in measures:
      _give_dominant_to([measure], [new_measure])

   return new_measure 
