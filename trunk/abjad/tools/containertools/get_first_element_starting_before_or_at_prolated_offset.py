from abjad.tools import durtools


def get_first_element_starting_before_or_at_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Get first `container` element starting before or at `prolated_offset`::
   
      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> containertools.get_first_element_starting_before_or_at_prolated_offset(staff, Duration(1, 8))
      Note("d'8")

   Return component.

   Return none when no `container` element starts before or at `prolated_offset`.

   .. versionchanged:: 1.1.2
      renamed ``containertools.get_rightmost_element_starting_not_after_prolated_offset( )`` to
      ``containertools.get_first_element_starting_before_or_at_prolated_offset( )``.
   '''

   prolated_offset = durtools.Duration(prolated_offset)

   for element in reversed(container):
      if element._offset.start <= prolated_offset:
         return element
