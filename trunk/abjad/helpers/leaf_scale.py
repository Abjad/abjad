from abjad.helpers.converge_to_power2 import _converge_to_power2
from abjad.helpers.duration_token_decompose import _duration_token_decompose
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


### NOTE: (or rather questions) 
### - would this be better named leaf_reset_duration( )?... 
###   we are not really scaling.
### - should multipliers be retained in setting of new duration ?
### - change ValueError in non notehead-assignable notes to InvalidDurationError?

def leaf_scale(dur, leaf):
   '''
      Example:
      
      >>> leaf_scale((5, 13), Note(0, (1, 8)))
      FixedDurationTuplet((5, 13), [Note(0, (1, 4))])
   '''
   assert isinstance(leaf, _Leaf) 
   dur = Rational(*_duration_token_unpack(dur))
   assert dur > 0
   try:
      #leaf.duration = dur
      leaf.duration.written = dur
      return leaf
   except ValueError:
      #leaf.duration = _converge_to_power2(leaf.duration, dur)
      leaf.duration.written = _converge_to_power2(leaf.duration.written, dur)
      result = FixedDurationTuplet(dur, [leaf])
      return result


from abjad.tie.spanner import Tie
def leaf_scale_binary(dur, leaf):
   '''
      Example:
      
      >>> leaf_scale_binary((5, 16), Note(0, (1, 8)))
      [Note(0, (1, 4), Note(0, (1,16)]
   '''
   assert isinstance(leaf, _Leaf)
   dur = Rational(*_duration_token_unpack(dur))
   assert dur > 0
   try:
      #leaf.duration = dur
      leaf.duration.written = dur
      return [leaf]
   except ValueError:
      result = [ ]
      for wd in _duration_token_decompose(dur):
         l = leaf.copy( )
         #l.duration.written = wd
         l.duration.written = Rational(*wd)
         result.append( l )
      parent = leaf._parent
      if parent:
         for l in result:
            #l.spanners.die( )
            l.spanners.clear( )
         indx = parent.index(leaf)
         parent.embed(indx, result)
         parent.pop(len(result) + indx)
      ### tie leaves
      for l in result:
         l.tie = None
      if not l.tie.spanner:
         Tie(result)
      ### remove dynamics and articulations from tied leaves.
      for n in result[1:]:
         n.dynamics = None
         n.articulations = None
      ### remove afterGrace from all but the last leaf
      ### and Grace all but the first leaf
      for n in result[:-1]:
         n.grace.after = None
      for n in result[1:]:
         n.grace.before = None
      return result
