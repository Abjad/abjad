from abjad.components._Leaf import _Leaf
from abjad.core import Rational
from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools.tuplettools.fix_contents_of_tuplets_in_expr import fix_contents_of_tuplets_in_expr
from abjad.tools.tuplettools.is_proper_tuplet_multiplier import is_proper_tuplet_multiplier
from abjad.components._Tuplet import FixedDurationTuplet
from abjad.components._Tuplet import FixedMultiplierTuplet


def scale_contents_of_tuplets_in_expr_by_multiplier(tuplet, multiplier):
   '''Scale fixed-duration tuplet by multiplier.
      Preserve tuplet multiplier.
      Return tuplet.
   '''

   # check input
   if isinstance(tuplet, FixedMultiplierTuplet):
      raise NotImplemented
   elif not isinstance(tuplet, FixedDurationTuplet):
      raise ValueError('must be tuplet.')
   assert isinstance(multiplier, Rational)

   # find new target duration
   old_target_duration = tuplet.duration.target
   new_target_duration = multiplier * old_target_duration

   # change tuplet target duration
   tuplet.duration.target = new_target_duration

   # if multiplier is note head assignable, scale contents graphically
   if durtools.is_assignable_rational(multiplier):
      for component in tuplet[:]:
         if isinstance(component, _Leaf):
            leaftools.scale_leaf_preprolated_duration(component, multiplier)

   # otherwise doctor up tuplet multiplier, if necessary
   elif not is_proper_tuplet_multiplier(tuplet.duration.multiplier):
         fix_contents_of_tuplets_in_expr(tuplet)

   # return tuplet
   return tuplet 
