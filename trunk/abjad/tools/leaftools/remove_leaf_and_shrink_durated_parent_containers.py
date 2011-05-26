from abjad.components import Measure
from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools.componenttools.get_proper_parentage_of_component import get_proper_parentage_of_component
from abjad.tools.componenttools.remove_component_subtree_from_score_and_spanners import remove_component_subtree_from_score_and_spanners
from abjad.tools.metertools import Meter
from fractions import Fraction


def remove_leaf_and_shrink_durated_parent_containers(leaf):
   r'''.. versionadded:: 1.1.1

   Remove `leaf` and shrink durated parent containers::

      abjad> measure = Measure((4, 8), tuplettools.FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 2)
      abjad> macros.diatonicize(measure)
      abjad> spannertools.BeamSpanner(measure.leaves)
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
   from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet

   prolated_leaf_duration = leaf.duration.prolated
   prolations = leaf.duration._prolations
   cur_prolation, i = Fraction(1), 0
   parent = leaf._parentage.parent

   while parent is not None and not parent.is_parallel:
      cur_prolation *= prolations[i]
      if isinstance(parent, FixedDurationTuplet):
         candidate_new_parent_dur = parent.duration.target - cur_prolation * leaf.duration.written
         if Fraction(0) < candidate_new_parent_dur:
            parent.duration.target = candidate_new_parent_dur
      elif isinstance(parent, Measure):
         old_denominator = parent._explicit_meter.denominator
         naive_meter = parent._explicit_meter.duration - prolated_leaf_duration
         better_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(
            naive_meter, old_denominator)
         parent._attach_explicit_meter(*better_meter)
         new_denominator = parent._explicit_meter.denominator

         old_prolation = durtools.positive_integer_to_implied_prolation_multipler(old_denominator)
         new_prolation = durtools.positive_integer_to_implied_prolation_multipler(new_denominator)
         adjusted_prolation = old_prolation / new_prolation
         for x in parent:
            if isinstance(x, FixedDurationTuplet):
               x.duration.target *= adjusted_prolation
            else:
               if adjusted_prolation != 1:
                  new_target = x.duration.preprolated * adjusted_prolation
                  FixedDurationTuplet(new_target, [x])
      parent = parent._parentage.parent
      i += 1
   parentage = get_proper_parentage_of_component(leaf)
   remove_component_subtree_from_score_and_spanners([leaf])
   for x in parentage:
      if not len(x):
         remove_component_subtree_from_score_and_spanners([x])
      else:
         break
