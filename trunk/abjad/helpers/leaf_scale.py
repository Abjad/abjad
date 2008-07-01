from abjad.duration.rational import Rational
from abjad.helpers.converge_to_power2 import converge_to_power2
from abjad.helpers.duration_token_decompose import _duration_token_decompose
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.leaf.leaf import _Leaf
from abjad.tuplet.fd.tuplet import FixedDurationTuplet
from abjad.containers.sequential import Sequential

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
      leaf.duration = dur
      return leaf
   except ValueError:
      leaf.duration = converge_to_power2(leaf.duration, dur)
      result = FixedDurationTuplet(dur, [leaf])
      return result


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
      leaf.duration = dur
      return leaf
   except ValueError:
      result = [ ]
      parent = leaf._parent
      if parent:
         indx = parent.index(leaf)
         leaf = parent.pop(indx)
         leaf.spanners.die( )
      for wd in _duration_token_decompose(dur):
         leaf = leaf.copy( )
         leaf.duration.written = wd
         result.append( leaf )
      ### tie leaves
      for n in result[0:-1]:
         n.tie = True
      if parent:
         ### TODO do we want these to be inside a Sequential?
         #result = Sequential(result)
         parent.embed(indx, result)
      return result
