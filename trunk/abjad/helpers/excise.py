from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.measure import Measure
from abjad.rational.rational import Rational
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def excise(leaf):
   '''Remove leaf from all sequential containers in leaf's parentage;
      shrink duration of any enclosing durated containers.
   '''
   prolated_leaf_duration = leaf.duration.prolated
   prolations = leaf.duration.prolations
   cur_prolation, i = Rational(1), 0
   parent = leaf._parent
   while parent is not None and not parent.parallel:
      cur_prolation *= prolations[i]
      if isinstance(parent, FixedDurationTuplet):
         #candidate_new_parent_dur = parent.duration - cur_prolation * leaf.duration
         #candidate_new_parent_dur = parent.duration.target - cur_prolation * leaf.duration
         candidate_new_parent_dur = parent.duration.target - cur_prolation * leaf.duration.written
         if candidate_new_parent_dur > Rational(0):
            #parent.duration = candidate_new_parent_dur
            parent.duration.target = candidate_new_parent_dur
      elif isinstance(parent, Measure):
         old_denominator = parent.meter.denominator
         naive_meter = parent.meter.duration - prolated_leaf_duration
         better_meter = _in_terms_of(naive_meter, old_denominator)
         parent.meter = better_meter
         new_denominator = parent.meter.denominator

         old_prolation = _denominator_to_multiplier(old_denominator)
         new_prolation = _denominator_to_multiplier(new_denominator)
         adjusted_prolation = old_prolation / new_prolation
         for x in parent:
            if isinstance(x, FixedDurationTuplet):
               #x.duration *= adjusted_prolation
               x.duration.target *= adjusted_prolation
            else:
               #FixedDurationTuplet(x.duration * adjusted_prolation, [x])
               # NOTE: not sure about following one line:
               FixedDurationTuplet(
                  x.duration.preprolated * adjusted_prolation, [x])
      parent = parent._parent
      i += 1
   parentage = leaf._parentage._parentage
   leaf._die( )
   for x in parentage:
      if not len(x):
         x._die( )
      else:
         break
