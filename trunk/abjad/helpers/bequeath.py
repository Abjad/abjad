from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_parent_and_indices import get_parent_and_indices
from abjad.helpers.give_dominant_spanners_to import \
   _give_dominant_spanners_to
from abjad.helpers.withdraw_from_crossing_spanners import \
   _withdraw_from_crossing_spanners


## TODO: Rename bequeath(donors, recipients) to replace(donors, recipients). ##

def bequeath(donor_components, recipient_components):
   '''Give everything from donor_components to recipient_components.
      Almost exactly the same as container setitem logic.
      This helper works with orphan donor_components.
      Container setitem logic can not work with orphan donor_components.
      Return donor_components.'''

   ## check input
   assert_components(donor_components, contiguity = 'strict', share = 'parent')
   assert_components(
      recipient_components, contiguity = 'strict', share = 'parent')

   ## handle empty input
   if len(donor_components) == 0:
      return donor_components

   ## get parent of donor components and indices of donor components in parent
   parent, start, stop = get_parent_and_indices(donor_components)

   ## if donor components have a parent, use setitem logic
   if parent:
      parent[start:stop+1] = recipient_components
      return donor_components

   ## otherwise
   else:

      ## give spanners that dominate donor components to recipient components
      _give_dominant_spanners_to(donor_components, recipient_components)

      ## withdraw donor components from crossing spanners
      _withdraw_from_crossing_spanners(donor_components)

   ## return donor components
   return donor_components
