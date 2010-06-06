from abjad.leaf import _Leaf
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools.tuplettools.contents_fix import contents_fix
from abjad.tuplet import FixedDurationTuplet
from abjad.tuplet import FixedMultiplierTuplet


def contents_scale(tuplet, multiplier):
   '''Scale fixed-duration tuplet by multiplier.
      Preserve tuplet multiplier.
      Return tuplet.'''

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
   if durtools.is_assignable_duration(multiplier):
      for component in tuplet[:]:
         if isinstance(component, _Leaf):
            leaftools.scale_leaf_preprolated_duration(component, multiplier)

   # otherwise doctor up tuplet multiplier, if necessary
   elif not durtools.is_tuplet_multiplier(tuplet.duration.multiplier):
         contents_fix(tuplet)

   # return tuplet
   return tuplet 
