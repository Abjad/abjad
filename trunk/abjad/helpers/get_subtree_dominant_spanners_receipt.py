from abjad.component.component import _Component
from abjad.helpers.assert_components import _assert_components
from abjad.helpers.iterate import iterate


def _get_subtree_dominant_spanners_receipt(subtrees):
   '''Return Python list of (spanner, index) pairs.
      Each (spanner, index) pair gives a spanner which dominates
      all components in 'subtrees' together with the start-index
      at which spanner first encounters 'subtrees'.

      Use this helper to 'lift' any and all spanners temporarily
      from 'subtrees', perform some action to the underlying
      score tree, and then reattach all spanners to new
      score components.
 
      TODO: Return custom _MultispannerReceipt instance.'''

   _assert_components(subtrees, contiguity = 'thread')

   first, last = subtrees[0], subtrees[-1]
   subtree_begin = first.offset.score
   subtree_end = last.offset.score + last.duration.prolated

   receipt = [ ]
   for component in iterate(first, _Component):
      if component.offset.score == subtree_begin:
         for spanner in component.spanners.attached:
            if spanner.begin <= subtree_begin:
               if subtree_end <= spanner.end:
                  index = spanner.index(component)
                  receipt.append((spanner, index))
      elif subtree_begin < component.offset.score:
         break

   return receipt
