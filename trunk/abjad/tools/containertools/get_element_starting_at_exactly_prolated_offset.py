from abjad.exceptions import MissingComponentError


def get_element_starting_at_exactly_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return `container` element starting at exactly `prolated_offset`::

      abjad> voice = Voice(construct.scale(8))
      abjad> containertools.get_element_start_at_prolated_offset(voice, Rational(6, 8))
      Note(b', 8)
   
   Raise missing component error when no `container` element starts
   at exactly `prolated_offset`::

      abjad> voice = Voice(construct.scale(8))
      abjad> containertools.get_element_start_at_prolated_offset(voice, Rational(15, 8))
      MissingComponentError

   .. versionchanged:: 1.1.2
      renamed ``containertools.get_element_starting_at_prolated_offset( )`` to
      ``containertools.get_element_starting_at_exactly_prolated_offset( )``.
   '''

   for element in container:
      if element.offset.prolated.start == prolated_offset:
         return element
   
   raise MissingComponentError
