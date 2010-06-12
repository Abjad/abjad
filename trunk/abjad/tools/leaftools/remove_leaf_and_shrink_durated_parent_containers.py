from abjad.measure import RigidMeasure
from abjad.meter import Meter
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools.componenttools.remove_component_subtree_from_score_and_spanners import remove_component_subtree_from_score_and_spanners
from abjad.tuplet import FixedDurationTuplet


def remove_leaf_and_shrink_durated_parent_containers(leaf):
   r'''Remove `leaf` and shrink durated parent containers::

      abjad> measure = RigidMeasure((4, 8), FixedDurationTuplet((2, 8), construct.run(3)) * 2)
      abjad> pitchtools.diatonicize(measure)
      abjad> Beam(measure.leaves)
      abjad> f(measure)
      {
         \time 4/8
         \times 2/3 {
            c'8 [
            d'8
            e'8
         }
         \times 2/3 {
            f'8
            g'8
            a'8 ]
         }
      }
      
   ::
      
      abjad> leaftools.remove_leaf_and_shrink_durated_parent_containers(measure.leaves[0])

   ::

      abjad> f(measure)
      {
         \time 5/12
         \scaleDurations #'(2 . 3) {
            {
               d'8 [
               e'8
            }
            {
               f'8
               g'8
               a'8 ]
            }
         }
      }

   Return none.
   '''

   prolated_leaf_duration = leaf.duration.prolated
   prolations = leaf.duration._prolations
   cur_prolation, i = Rational(1), 0
   parent = leaf.parentage.parent

   while parent is not None and not parent.parallel:
      cur_prolation *= prolations[i]
      if isinstance(parent, FixedDurationTuplet):
         candidate_new_parent_dur = parent.duration.target - \
            cur_prolation * leaf.duration.written
         if candidate_new_parent_dur > Rational(0):
            parent.duration.target = candidate_new_parent_dur
      elif isinstance(parent, RigidMeasure):
         old_denominator = parent.meter.forced.denominator
         naive_meter = parent.meter.forced.duration - prolated_leaf_duration
         better_meter = durtools.in_terms_of(naive_meter, old_denominator)
         parent.meter.forced = Meter(better_meter)
         new_denominator = parent.meter.forced.denominator

         old_prolation = durtools.denominator_to_multiplier(old_denominator)
         new_prolation = durtools.denominator_to_multiplier(new_denominator)
         adjusted_prolation = old_prolation / new_prolation
         for x in parent:
            if isinstance(x, FixedDurationTuplet):
               x.duration.target *= adjusted_prolation
            else:
               if adjusted_prolation != 1:
                  new_target = x.duration.preprolated * adjusted_prolation
                  FixedDurationTuplet(new_target, [x])
      parent = parent.parentage.parent
      i += 1
   parentage = leaf.parentage.parentage[1:]
   remove_component_subtree_from_score_and_spanners([leaf])
   for x in parentage:
      if not len(x):
         remove_component_subtree_from_score_and_spanners([x])
      else:
         break
