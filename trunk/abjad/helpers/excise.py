from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from abjad.helpers.in_terms_of import _in_terms_of
#from abjad.measure.measure import Measure
#from abjad.measure.prolating.measure import ProlatingMeasure
from abjad.measure.rigid.measure import RigidMeasure
from abjad.rational.rational import Rational
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


### TODO: Rather than branching on each of the different types of container,
###       does it make more sense to implement a private _excise( ) method
###       on each of the different container types?

def excise(leaf):
   '''
   Remove leaf from all sequential containers in leaf's parentage;
   shrink duration of any enclosing durated containers.
   '''

   prolated_leaf_duration = leaf.duration.prolated
   prolations = leaf.duration._prolations
   cur_prolation, i = Rational(1), 0
   parent = leaf._parent

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
         better_meter = _in_terms_of(naive_meter, old_denominator)
         parent.meter = better_meter
         new_denominator = parent.meter.forced.denominator

         old_prolation = _denominator_to_multiplier(old_denominator)
         new_prolation = _denominator_to_multiplier(new_denominator)
         adjusted_prolation = old_prolation / new_prolation
         for x in parent:
            if isinstance(x, FixedDurationTuplet):
               x.duration.target *= adjusted_prolation
            else:
               if adjusted_prolation != 1:
                  new_target = x.duration.preprolated * adjusted_prolation
                  FixedDurationTuplet(new_target, [x])
      parent = parent._parent
      i += 1
   parentage = leaf.parentage.parentage[1:]
   leaf.detach( )
   for x in parentage:
      if not len(x):
         x.detach( )
      else:
         break
