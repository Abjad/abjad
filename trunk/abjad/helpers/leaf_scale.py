from abjad.leaf.leaf import _Leaf
from converge_to_power2 import converge_to_power2
from .. duration.rational import Rational
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from .. tuplet.fd.tuplet import FixedDurationTuplet
### NOTE: (or rather questions) 
### - should multipliers be retained in scaling ?
### - change ValueError in non notehead-assignable notes to InvalidDurationError?

def leaf_scale(new_dur, leaf):
   '''
      Example:
      
      >>> leaf_scale((5, 13), Note(0, (1, 8)))
      FixedDurationTuplet((5, 13), [Note(0, (1, 4))])
   '''
   assert isinstance(leaf, _Leaf) 
   new_dur = Rational(*_duration_token_unpack(new_dur))
   assert new_dur > 0
   ### NOTE - if stuff starts to break later on in the implementation of scopy,
   ###        consider changing leaf.duration to leaf.duration.prolated, etc.
   try:
      leaf.duration = new_dur
      return leaf
   except ValueError:
      leaf.duration = converge_to_power2(leaf.duration, new_dur)
      result = FixedDurationTuplet(new_dur, [leaf])
      return result


