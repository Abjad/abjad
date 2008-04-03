from abjad.duration.rational import Rational
from abjad.helpers.denominator_to_multiplier import _denominator_to_multiplier
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.measure.measure import Measure
from abjad.tuplet.fd.tuplet import FixedDurationTuplet

### TODO -- don't know if this works yet with *nested* tuplets
###         don't know if this works with fixed *multiplier* tuplets
###         don't know if this works with plain vanilla containers

def excise(leaf):
   '''Remove leaf from all sequential containers in leaf's parentage;
      shrink duration of any enclosing durated containers.
   '''
   prolated_leaf_duration = leaf.duration.prolated
   prolations = leaf.duration.prolations
   print prolations
   cur_prolation, i = Rational(1), 0
   parent = leaf._parent
   while parent is not None and not parent.parallel:
      cur_prolation *= prolations[i]
      print cur_prolation
      if isinstance(parent, FixedDurationTuplet):
         if len(parent) > 1:
#            immediate_parent_prolated = parent.duration.multiplier * \
#               leaf.duration
#            parent.duration -= immediate_parent_prolated
            parent.duration -= cur_prolation * leaf.duration
         else:
            pass
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
               x.duration *= adjusted_prolation
            else:
               FixedDurationTuplet(x.duration * adjusted_prolation, [x])
      parent = parent._parent
      i += 1
   ### TODO - will probably need to generalize this parent-killing loop
   ###        to make nested tuplets work
   if len(leaf._parent) == 1:
      leaf._parent._die( )
   leaf._die( )
