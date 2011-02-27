from abjad.components import Container
from abjad.exceptions import MusicContentsError
from abjad.tools.componenttools._give_music_from_donor_components_to_recipient_components import \
   _give_music_from_donor_components_to_recipient_components
from abjad.tools.componenttools._give_donor_components_position_in_parent_to_recipient_components import \
   _give_donor_components_position_in_parent_to_recipient_components
from abjad.tools.spannertools._give_spanners_that_dominate_donor_components_to_recipient_components import _give_spanners_that_dominate_donor_components_to_recipient_components


def move_parentage_children_and_spanners_from_components_to_empty_container(donors, recipient):
   '''This helper hands over music, if any.

   .. versionchanged:: 1.1.2
      renamed ``scoretools.donate( )`` to
      ``containertools.move_parentage_children_and_spanners_from_components_to_empty_container( )``.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_contiguous_components_in_same_parent(donors)

   if not isinstance(recipient, Container):
      raise TypeError
   
   if not len(recipient) == 0:
      raise MusicContentsError

   _give_music_from_donor_components_to_recipient_components(donors, recipient)
   _give_spanners_that_dominate_donor_components_to_recipient_components(donors, [recipient])
   _give_donor_components_position_in_parent_to_recipient_components(donors, [recipient])
