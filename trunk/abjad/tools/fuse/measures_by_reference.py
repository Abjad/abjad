from abjad.measure.measure import _Measure
from abjad.measure.rigid.measure import RigidMeasure
from abjad.meter.meter import Meter
from abjad.tools import check
from abjad.tools import containertools
from abjad.tools import metertools
from abjad.tools import parenttools
from abjad.tools.parenttools.switch import _switch
from abjad.tools.spannertools.give_dominant_to import _give_dominant_to


def measures_by_reference(measures):
   '''Measures in 'measures' must be strictly parent-contiguous.
      Measure fusion across intervening container boundaries is undefined.
      Calculate best new time signature and instantiate new measure.
      Give contents of 'measures' to new measure.
      Give dominant spanners of 'measures' to new measure.
      Give parentage of 'measures' to new measure.
      'Measures' end up empty, orphaned and spannerless.'''

   check.assert_components(measures, 
      klasses = (_Measure), contiguity = 'strict', share = 'parent')

   if len(measures) == 0:
      return None

   if len(measures) == 1:
      return measures[0]

   parent, start, stop = parenttools.get_with_indices(measures)

   old_denominators = [x.meter.effective.denominator for x in measures]
   new_duration = sum([x.meter.effective.duration for x in measures])

   new_meter = metertools.make_best(new_duration, old_denominators)

   music = [ ]
   for measure in measures:
      multiplier = ~new_meter.multiplier * measure.meter.effective.multiplier
      measure_music = measure[:]
      containertools.contents_scale(measure_music, multiplier)
      music += measure_music

   _switch(music, None)
   new_measure = RigidMeasure(new_meter, music)
   _switch(measures, None)
   parent.insert(start, new_measure)

   for measure in measures:
      _give_dominant_to([measure], [new_measure])

   return new_measure 
