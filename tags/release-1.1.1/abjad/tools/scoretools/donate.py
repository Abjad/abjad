from abjad.tools import check
from abjad.tools.componenttools.give_music_to import _give_music_to
from abjad.tools.parenttools.give_position_to import _give_position_to
from abjad.tools.spannertools.give_dominant_to import _give_dominant_to


def donate(donors, recipient):
   '''This helper hands over music, if any.'''

   check.assert_components(donors, contiguity = 'strict', share = 'parent')

   _give_music_to(donors, recipient)
   _give_dominant_to(donors, [recipient])
   _give_position_to(donors, [recipient])
