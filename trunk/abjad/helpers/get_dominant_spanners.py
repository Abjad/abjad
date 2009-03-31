from abjad.component.component import _Component
from abjad.helpers.assert_components import assert_components
from abjad.helpers.iterate import iterate


def get_dominant_spanners(components):
   '''Return Python list of (spanner, index) pairs.
      Each (spanner, index) pair gives a spanner which dominates
      all components in 'components' together with the start-index
      at which spanner first encounters 'components'.

      Use this helper to 'lift' any and all spanners temporarily
      from 'components', perform some action to the underlying
      score tree, and then reattach all spanners to new
      score components.

      This operation always leaves all expressions in tact.'''

   assert_components(components, contiguity = 'thread')

   if len(components) == 0:
      return [ ]

   first, last = components[0], components[-1]
   subtree_begin = first.offset.score
   subtree_end = last.offset.score + last.duration.prolated

   receipt = set([ ])
   for component in iterate(first, _Component):
      if component.offset.score == subtree_begin:
         for spanner in component.spanners.attached:
            if spanner.begin <= subtree_begin:
               if subtree_end <= spanner.end:
                  index = spanner.index(component)
                  receipt.add((spanner, index))
      elif subtree_begin < component.offset.score:
         break

   return receipt
