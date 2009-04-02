from abjad.helpers.leaf_scale_binary import leaf_scale_binary
from abjad.helpers.iterate import iterate


def leaves_fuse_binary(data):
   '''Fuse duration of all leaves in <data> into a single leaf, 
      if possible. Only properties of the first leaf are kept.'''

   ## are all the leaves in data siblings? do we care.
   ## are they beads of the same thread?
   ## TODO: Change naive iteration in leaves_fuse_binary( ) to bead nav. ##
   from abjad.leaf.leaf import _Leaf
   leaves = list(iterate(data, _Leaf))
   if len(leaves) == 1:
      return leaves
   elif len(leaves) > 1:
      dur = 0
      for l in leaves:
         dur += l.duration.written
      ## delete all but the first
      for l in leaves[1:]:
         l.detach( )
      return leaf_scale_binary(leaves[0], dur)
