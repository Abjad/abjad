from abjad.helpers.assess_components import assess_components
from abjad.helpers.container_scale import container_scale
from abjad.helpers.is_measure_list import _is_measure_list
from abjad.measure.rigid.measure import RigidMeasure
from abjad.meter.meter import Meter
from abjad.tools.parenttools.switch import _switch
from abjad.tools import metertools
from abjad.tools import parenttools
from abjad.tools.spannertools.give_dominant_to import _give_dominant_to


def measures_fuse(measure_list):
   '''Fuse measures in measure_list.
      Calculate best new time signature.'''

   assert _is_measure_list(measure_list)

   if len(measure_list) == 0:
      return None

   if len(measure_list) == 1:
      return measure_list[0]

   parent, parent_index, stop_index = parenttools.get_with_indices(measure_list)

   old_denominators = [x.meter.effective.denominator for x in measure_list]
   new_duration = sum([x.meter.effective.duration for x in measure_list])

   new_meter = metertools.make_best(new_duration, old_denominators)

   music = [ ]
   for measure in measure_list:
      multiplier = ~new_meter.multiplier * measure.meter.effective.multiplier
      measure_music = measure[:]
      container_scale(measure_music, multiplier)
      music += measure_music

   _switch(music, None)
   new_measure = RigidMeasure(new_meter, music)
   _switch(measure_list, None)
   parent.insert(parent_index, new_measure)

   for measure in measure_list:
      _give_dominant_to([measure], [new_measure])

   return new_measure 
