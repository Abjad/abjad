from attributes import _transfer_all_attributes
from .. duration.rational import Rational
from leaf_scale import leaf_scale
from abjad.leaf.leaf import _Leaf

def leaf_split(split_dur, leaf):
   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, (int, list, tuple, Rational))
   if isinstance(split_dur, (list, tuple)):
      split_dur = Rational(*split_dur)

   if split_dur == 0 or split_dur >= leaf.duration:
      return [leaf]
   else:
      l1 = leaf.copy()
      l1.spanners.die()
      parent = leaf._parent
      if parent:
         indx = parent.index(leaf)
         parent.embed(indx, l1)

      l1 = leaf_scale(split_dur, l1)
      l2 = leaf_scale(leaf.duration - split_dur, leaf)
      return [l1, l2]
