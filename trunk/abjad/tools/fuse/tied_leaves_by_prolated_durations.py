from abjad.tools import componenttools
from abjad.tools import tietools
from abjad.tools.fuse.leaves_in_tie_chain import leaves_in_tie_chain


def tied_leaves_by_prolated_durations(components, prolated_durations):
   r'''Fuse `components` tied leaves by `prolated_durations`::

      abjad> staff = Staff(leaftools.make_repeated_notes(8))
      abjad> Tie(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'8 ~
         c'8 ~
         c'8 ~
         c'8 ~
         c'8 ~
         c'8 ~
         c'8
      }
      
   ::
      
      abjad> fuse.tied_leaves_by_prolated_durations(staff, [Rational(3, 8), Rational(3, 8)])

   ::
 
      abjad> f(staff)
      \new Staff {
         c'4. ~
         c'4. ~
         c'8 ~
         c'8
      }

   Return none.
   '''

   ## get duration groups
   groups = componenttools.partition_components_by_prolated_durations(
      components, prolated_durations, fill = 'exact', cyclic = False, overhang = False)

   for group in groups:
      ## get tie_chains intersecting this group
      tie_chains = tietools.get_tie_chains(group)

      for chain in tie_chains:
         leaves_in_tie_chain(chain)
