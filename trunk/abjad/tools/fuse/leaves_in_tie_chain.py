from abjad.tools import tietools
from abjad.tools.fuse.leaves_by_reference import leaves_by_reference


def leaves_in_tie_chain(tie_chain):
   r'''Fuse leaves in `tie_chain` by parent::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> Tie(staff.leaves)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8 ~
            c'8 ~
         }
         {
            \time 2/8
            c'8 ~
            c'8
         }
      }
      
   ::
      
      abjad> fuse.leaves_in_tie_chain(staff.leaves[0].tie.chain)
      [[Note(c', 4)], [Note(c', 4)]]

   ::

      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'4 ~
         }
         {
            \time 2/8
            c'4
         }
      }

   Return list of fused notes by parent.

   .. todo:: rename ``fuse.tied_leaves_by_parent( )``.

   .. todo:: rename ``tietools.fuse_tied_leaves_by_parent( )``?
   '''

   ## check input
   if not tietools.is_chain(tie_chain):
      raise TypeError('must be tie chain.')

   ## init result
   result = [ ]

   ## group leaves in tie chain by parent
   parts = tietools.group_by_parent(tie_chain)
   
   ## fuse leaves in each part
   for part in parts:
      result.append(leaves_by_reference(part))

   ## return result
   return result
