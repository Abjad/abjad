from abjad.tools import check
from abjad.tools.tietools.is_chain import is_chain


def is_in_same_parent(expr):
   r'''True when expr is a tie chain with all leaves in same parent.

      That is, True when tie chain crosses no container boundaries,
      otherwise False.

      Example::

         abjad> t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
         abjad> Tie(t.leaves[1:3])

         \new Staff {
               \time 2/8
               c'8
               c'8 ~
               \time 2/8
               c'8
               c'8
         }

         abjad> assert tietools.is_in_same_parent(t.leaves[0].tie.chain)
         abjad> assert not tietools.is_in_same_parent(t.leaves[1].tie.chain)
         abjad> assert not tietools.is_in_same_parent(t.leaves[2].tie.chain)
         abjad> assert tietools.is_in_same_parent(t.leaves[3].tie.chain)
   '''

   return is_chain(expr) and \
      check.assess_components(list(expr), share = 'parent')
