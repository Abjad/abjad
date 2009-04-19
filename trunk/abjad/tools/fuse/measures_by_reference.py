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
   '''Fuse measures in measures.
      Calculate best new time signature.'''

   check.assert_components(
      measures, klasses = (_Measure), contiguity = 'thread')

   if len(measures) == 0:
      return None

   if len(measures) == 1:
      return measures[0]

   parent, parent_index, stop_index = parenttools.get_with_indices(measures)

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
   parent.insert(parent_index, new_measure)

   for measure in measures:
      _give_dominant_to([measure], [new_measure])

   return new_measure 
