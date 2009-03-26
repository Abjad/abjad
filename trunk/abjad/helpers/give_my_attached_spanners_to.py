from abjad.helpers.assert_components import assert_components


def _give_my_attached_spanners_to(donor_component, recipient_components):
   '''Find all spanners attaching directly to 'donor_component'.
      Insert each component in 'recipient_components' into
      each spanner attaching directly to 'donor_component'.
      Remove 'donor_component' from each attaching spanner.
      Return 'donor_component'.

      Not composer-safe.'''

   assert_components([donor_component])
   assert_components(recipient_components, contiguity = 'thread')
   
   attached_spanners = list(donor_component.spanners.attached)
   for attached_spanner in attached_spanners:
      donor_index = attached_spanner.index(donor_component)
      for recipient_component in reversed(recipient_components):
         attached_spanner._insert(donor_index, recipient_component)
      attached_spanner._remove(donor_component)

   return donor_component
