from abjad.helpers.assert_components import assert_components
from abjad.helpers.give_spanned_music_from_to import \
   _give_spanned_music_from_to
from abjad.tools import parenttools
from abjad.tools.spannertools.give_dominant_to import _give_dominant_to


def donate(donors, recipient):
   '''This helper hands over music, if any.'''

   assert_components(donors, contiguity = 'strict', share = 'parent')

   _give_spanned_music_from_to(donors, recipient)
   _give_dominant_to(donors, [recipient])
   parenttools.give_position_to(donors, [recipient])
