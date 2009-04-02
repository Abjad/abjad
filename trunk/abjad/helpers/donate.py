from abjad.helpers.assert_components import assert_components
from abjad.helpers.give_dominant_spanners_to import \
   _give_dominant_spanners_to 
from abjad.helpers.give_position_in_parent_from_to import \
   _give_position_in_parent_from_to
from abjad.helpers.give_spanned_music_from_to import \
   _give_spanned_music_from_to


def donate(donors, recipient):
   '''Docs.
      This was previously _Component.bequeath( ).
      This helper hands over music, if any.'''

   assert_components(donors, contiguity = 'strict', share = 'parent')

   _give_spanned_music_from_to(donors, recipient)
   _give_dominant_spanners_to(donors, [recipient])
   _give_position_in_parent_from_to(donors, [recipient])
