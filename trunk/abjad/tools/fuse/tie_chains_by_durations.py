from abjad.tools import durtools
from abjad.tools import tietools
from abjad.tools.fuse.leaves_in_tie_chain import leaves_in_tie_chain as \
   fuse__leaves_in_tie_chain
#from abjad.tools.fuse.leaves_by_reference import leaves_by_reference as \
#   fuse__leaves_by_reference


def tie_chains_by_durations(components, durations):
   '''Fuse all tied leaves that fall within each of the given durations.
   Returns None.'''

   ## get duration groups
   groups = durtools.group_prolated(components, durations, 
      fill = 'exact', cyclic = False, overhang = False)

   for group in groups:
      ## get tie_chains intersecting this group
      tie_chains = tietools.get_tie_chains(group)

      for chain in tie_chains:
         fuse__leaves_in_tie_chain(chain)
