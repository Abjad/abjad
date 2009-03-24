from abjad.component.component import _Component
from abjad.helpers.components_switch_parent_to import \
   _components_switch_parent_to


def _give_my_spanned_music_to(donor_component, recipient_component):
   '''If 'donor_component' has music and 'recipient_component'
      is an empty container, give music 'donor_component' to
      'recipient_component', leaving any spanners attaching
      to music of 'donor_component' in tact, including
      crossing spanners.

      If 'donor_component' has music and 'recipient_component'
      is not an empty container, raise TypeError.

      If 'donor_component' has no music, do nothing.

      Return 'donor_component'.

      Helper is not composer-safe and may cause discontiguous spanners.'''

   from abjad.container.container import Container

   if not isinstance(donor_component, _Component):
      raise TypeError('Donor component must be Abjad component.')

   if not isinstance(donor_component, Container):
      return donor_component

   if not len(donor_component):
      return donor_component

   if not isinstance(recipient_component, Container):
      raise TypeError('Recipient component must be Abjad container.')

   if not len(recipient_component) == 0:
      raise TypeError('Recipient component must be empty.')

   recipient_component._music.extend(donor_component[:])
   _components_switch_parent_to(recipient_component[:], recipient_component)

   return donor_component
