from .. duration.rational import Rational
from converge_to_power2 import converge_to_power2
from .. tuplet.fd.tuplet import FixedDurationTuplet
from abjad.leaf.leaf import _Leaf
### TODO: (or rather questions) 
### - should multipliers be retained in scaling ?
### - change ValueError in non notehead-assignable notes to InvalidDurationError?

def leaf_scale(new_dur, leaf):
   '''
      Example:
      
      >>> leaf_scale((5, 13), Note(0, (1, 8)))
      FixedDurationTuplet((5, 13), [Note(0, (1, 4))])
   '''
   assert isinstance(leaf, _Leaf) 
   assert isinstance(new_dur, (list, tuple, Rational))
   if isinstance(new_dur, (list, tuple)):
      new_dur = Rational(*new_dur)
   try:
      leaf.duration = new_dur
      return leaf
   except ValueError:
      leaf.duration = converge_to_power2(leaf.duration, new_dur)
      result = FixedDurationTuplet(new_dur, [leaf])
      return result


