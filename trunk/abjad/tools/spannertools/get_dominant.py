from abjad.component import _Component
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

   This operation always leaves all expressions in tact.
   '''

   check.assert_components(
      components, contiguity = 'thread', allow_orphans = False)

   receipt = set([ ])

   if len(components) == 0:
      return receipt
   
   first, last = components[0], components[-1]

#   subtree_begin = first.offset.prolated.start
#   subtree_end = last.offset.prolated.stop

#   for component in iterate.naive_forward(first, _Component):
#      if component.offset.prolated.start == subtree_begin:
#         for spanner in component.spanners.attached:
#            if spanner.offset.start <= subtree_begin:
#               if subtree_end <= spanner.offset.stop:
#                  index = spanner.index(component)
#                  receipt.add((spanner, index))
#      elif subtree_begin < component.offset.prolated.start:
#         break

   start_components = first._navigator._contemporaneousStartContents
   stop_components = set(last._navigator._contemporaneousStopContents)
   for component in start_components:
      for spanner in component.spanners.attached:
         if set(spanner[:]) & stop_components != set([ ]):
            index = spanner.index(component)
            receipt.add((spanner, index))

   return receipt
