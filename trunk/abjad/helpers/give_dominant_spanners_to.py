from abjad.helpers.assert_components import assert_components
from abjad.tools import spannertools


def _give_dominant_spanners_to(donor_components, recipient_components):
   '''Find all spanners dominating 'donor_components'.
      Insert each component in 'recipient_components' into
      each spanner dominating 'donor_components'.
      Remove 'donor_components' from each dominating spanner.
      Return 'donor_components'.

      Not composer-safe.'''

   assert_components(donor_components, contiguity = 'thread')
   assert_components(recipient_components, contiguity = 'thread')
   
   receipt = spannertools.get_dominant(donor_components)
   for spanner, index in receipt:
      for recipient_component in reversed(recipient_components):
         spanner._insert(index, recipient_component)
      for donor_component in donor_components:
         spanner._remove(donor_component)

   return donor_components
