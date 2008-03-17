from attributes import _transfer_all_attributes
from .. duration.rational import Rational
from leaf_scale import leaf_scale
from abjad import Note

def leaf_split(split_dur, leaf):
   assert leaf.kind('_Leaf')
   assert type(split_dur) in (int, list, tuple, Rational)
   if type(split_dur) in (list, tuple):
      split_dur = Rational(*split_dur)

   if split_dur == 0 or split_dur >= leaf.duration:
      return [leaf]
   else:
      l1 = leaf.copy()
      for s in l1.spanners.get():
         s.die()

      parent = leaf._parent
      if parent:
         indx = parent.index(leaf)
         parent.embed(indx, l1)

      l1 = leaf_scale(split_dur, l1)
      l2 = leaf_scale(leaf.duration - split_dur, leaf)
      return [l1, l2]
