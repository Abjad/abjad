from abjad.helpers.container_contents_scale import container_contents_scale
#from abjad.helpers.in_terms_of import _in_terms_of
from abjad.helpers.is_measure_list import _is_measure_list
from abjad.helpers.make_best_meter import _make_best_meter
from abjad.measure.rigid.measure import RigidMeasure
from abjad.meter.meter import Meter


def measures_fuse(measure_list):
   '''Fuse measures in measure_list.
      Calculate best new time signature.

      Better than naive spanner handling.'''

   assert _is_measure_list(measure_list)

   if len(measure_list) == 0:
      return None

   if len(measure_list) == 1:
      return measure_list[0]

   left = measure_list[0]
 
   if not left.parentage.orphan:
      parent = left.parentage.parent
      parent_index = parent.index(left)
   else:
      parent_index = None

   for measure in measure_list:
      measure.parentage.detach( )

   old_denominators = [x.meter.effective.denominator for x in measure_list]
   new_duration = sum([x.meter.effective.duration for x in measure_list])

   new_meter = _make_best_meter(new_duration, old_denominators)

   music = [ ]
   for measure in measure_list:
      multiplier = ~new_meter.multiplier * measure.meter.effective.multiplier
      measure_music = measure[:]
      container_contents_scale(measure_music, multiplier)
      music += measure_music

   for element in music:
      element.parentage.detach( )

   new_measure = RigidMeasure(new_meter, music)
   parent.insert(parent_index, new_measure)

   ## TODO: this is probably pretty good code to encapsulate for later use

   for i, measure in enumerate(measure_list):
      for spanner in list(measure.spanners.attached):
         spanner_index = spanner.index(measure)
         spanner[spanner_index] = new_measure
         subsequent_measures = measure_list[i:]
         for subsequent_measure in subsequent_measures:
            if subsequent_measure in spanner:
               spanner.remove(subsequent_measure)

   return new_measure 
