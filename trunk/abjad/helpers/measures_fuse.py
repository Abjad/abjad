from abjad.helpers.container_contents_scale import container_contents_scale
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.rigid.measure import RigidMeasure
from abjad.meter.meter import Meter


def measures_fuse(left, right):
   '''Create a new measure equal to left + right;
      Calculate time signature.

      Handles spanners in naive way.'''

   assert left.parentage.parent == right.parentage.parent

   if not left.parentage.orphan:
      parent = left.parentage.parent
      parent_index = parent.index(left)
   else:
      parent_index = None

   left.parentage.detach( )
   right.parentage.detach( )

   old_denominators = (left.meter.effective.denominator, \
      right.meter.effective.denominator)
   new_duration = left.meter.effective.duration + \
      right.meter.effective.duration
   new_pair = _in_terms_of(new_duration, min(old_denominators))
   if new_pair[1] != min(old_denominators):
      new_pair = _in_terms_of(new_pair, max(old_denominators))
   new_meter = Meter(new_pair)

   left_multiplier = ~new_meter.multiplier * left.meter.effective.multiplier
   left_music = left[:]
   container_contents_scale(left_music, left_multiplier)

   right_multiplier = ~new_meter.multiplier * right.meter.effective.multiplier
   right_music = right[:]
   container_contents_scale(right_music, right_multiplier)

   #music = left[:] + right[:]
   music = left_music + right_music

   for element in music:
      element.parentage.detach( )

   new_measure = RigidMeasure(new_pair, music)
   parent.insert(parent_index, new_measure)

   for spanner in list(left.spanners.attached):
      spanner_index = spanner.index(left)
      spanner[spanner_index] = new_measure
      if right in spanner:
         spanner.remove(right)

   for spanner in list(right.spanners.attached):
      spanner_index = spanner.index(right)
      spanner[spanner_index] = new_measure

   return new_measure 
