from abjad.tools import tietools
from abjad.tools.fuse.leaves_by_reference import leaves_by_reference as \
   fuse_leaves_by_reference


def leaves_in_tie_chain(tie_chain):
   '''Fuse leaves in tie chain with same immediate parent.'''

   ## check input
   if not tietools.is_chain(tie_chain):
      raise TypeError('must be tie chain.')

   ## init result
   result = [ ]

   ## group leaves in tie chain by parent
   parts = tietools.group_by_parent(tie_chain)
   
   ## fuse leaves in each part
   for part in parts:
      result.append(fuse_leaves_by_reference(part))

   ## return result
   return result
