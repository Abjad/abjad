from abjad.component.component import _Component
from abjad.tools import check
from abjad.tools import parenttools
from abjad.tools import iterate


def get_dominant(components):
   '''Return Python list of (spanner, index) pairs.
      Each (spanner, index) pair gives a spanner which dominates
      all components in 'components' together with the start-index
      at which spanner first encounters 'components'.

      Use this helper to 'lift' any and all spanners temporarily
      from 'components', perform some action to the underlying
      score tree, and then reattach all spanners to new
      score components.

      This operation always leaves all expressions in tact.'''

   check.assert_components(components, contiguity = 'thread', allow_orphans = False)
   receipt = set([ ])

   if len(components) == 0:
      return receipt
   
   first, last = components[0], components[-1]
   subtree_begin = first.offset.score
   subtree_end = last.offset.score + last.duration.prolated

   for component in iterate.naive(first, _Component):
      if component.offset.score == subtree_begin:
         for spanner in component.spanners.attached:
            if spanner.begin <= subtree_begin:
               if subtree_end <= spanner.end:
                  index = spanner.index(component)
                  receipt.add((spanner, index))
      elif subtree_begin < component.offset.score:
         break

   return receipt
