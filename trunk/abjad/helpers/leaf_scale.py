from .. duration.rational import Rational
from converge_to_power2 import converge_to_power2
from .. tuplet.fd.tuplet import FixedDurationTuplet
### TODO: (or rather questions) 
### - should multipliers be retained in scaling ?
### - change ValueError in non notehead-assignable notes to InvalidDurationError?

def leaf_scale(new_dur, leaf):
   '''
      Example:
      
      >>> leaf_scale((5, 13), Note(0, (1, 8)))
      FixedDurationTuplet((5, 13), [Note(0, (1, 4))])
   '''
   ### which is better: leaf.kind vs. isinstance?
   ### btw: should kind be private?
   #from abjad import _Leaf
   #assert isinstance(leaf, _Leaf) 
   assert leaf.kind('_Leaf')
   assert type(new_dur) in (list, tuple, Rational)
   if type(new_dur) in (list, tuple):
      new_dur = Rational(*new_dur)
   try:
      leaf.duration = new_dur
      return leaf
   except ValueError:
      leaf.duration = converge_to_power2(leaf.duration, new_dur)
#      parent = leaf._parent
#      if parent is not None:
#         indx = parent.index(leaf)
#         result = FixedDurationTuplet(new_dur, [leaf])
#         parent[indx] = result
#      else:
      result = FixedDurationTuplet(new_dur, [leaf])
      return result


