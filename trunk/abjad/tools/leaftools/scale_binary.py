from abjad.exceptions.exceptions import AssignabilityError
from abjad.helpers.bequeath import bequeath
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tie.spanner import Tie
from abjad.tools import clone
from abjad.tools import durtools 
from abjad.tools import iterate


## NOTE: (or rather questions) 
## - would this be better named leaf_reset_duration( )?... 
##   we are not really scaling.
## - should multipliers be retained in setting of new duration ?

def scale_binary(leaf, dur):
   '''Example:
      
      >>> leaftools.scale_binary(Note(0, (1, 8)), Rational(5, 16))
      [Note(0, (1, 4), Note(0, (1,16)]'''

   assert isinstance(leaf, _Leaf)
   assert isinstance(dur, Rational)
   assert dur > 0
   try:
      leaf.duration.written = dur
      return [leaf]
   except AssignabilityError:
      result = [ ]
      for wd in durtools.token_decompose(dur):
         l = clone.unspan([leaf])[0]
         l.duration.written = Rational(*wd)
         result.append(l)
      bequeath([leaf], result)
      ## tie leaves
      if not l.tie.parented:
         Tie(result)
      ## remove dynamics and articulations from tied leaves.
      for n in result[1:]:
         n.dynamics.mark = None
         n.articulations = None
      ## remove afterGrace from all but the last leaf
      ## and Grace all but the first leaf
      for n in result[:-1]:
         n.grace.after = None
      for n in result[1:]:
         n.grace.before = None
      return result
