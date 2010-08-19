from abjad.tools import componenttools
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def is_tie_chain_with_all_leaves_in_same_parent(expr):
   r'''True when expr is a tie chain with all leaves in same parent.

   That is, True when tie chain crosses no container boundaries,
   otherwise False.

   Example::

      abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> spannertools.TieSpanner(t.leaves[1:3])

      \new Staff {
            \time 2/8
            c'8
            c'8 ~
            \time 2/8
            c'8
            c'8
      }

      abjad> assert tietools.is_tie_chain_with_all_leaves_in_same_parent(t.leaves[0].tie.chain)
      abjad> assert not tietools.is_tie_chain_with_all_leaves_in_same_parent(t.leaves[1].tie.chain)
      abjad> assert not tietools.is_tie_chain_with_all_leaves_in_same_parent(t.leaves[2].tie.chain)
      abjad> assert tietools.is_tie_chain_with_all_leaves_in_same_parent(t.leaves[3].tie.chain)

   .. versionchanged:: 1.1.2
      renamed ``tietools.is_in_same_parent( )`` to
      ``tietools.is_tie_chain_with_all_leaves_in_same_parent( )``.
   '''

   return is_tie_chain(expr) and componenttools.all_are_components_in_same_parent(list(expr))
