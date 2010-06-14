from abjad.tools.componenttools.give_music_to import _give_music_to
from abjad.tools.parenttools.give_position_to import _give_position_to
from abjad.tools.spannertools.give_dominant_to import _give_dominant_to


def donate(donors, recipient):
   '''This helper hands over music, if any.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_contiguous_components_in_same_parent(donors)

   _give_music_to(donors, recipient)
   _give_dominant_to(donors, [recipient])
   _give_position_to(donors, [recipient])
