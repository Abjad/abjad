from fractions import Fraction


def get_first_element_starting_strictly_after_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return leftmost `container` element starting after `prolated_offset`::

      abjad> staff = Staff(macros.scale(4))
      abjad> containertools.get_first_element_starting_strictly_after_prolated_offset(staff, Fraction(1, 8))
      Note(e', 8)

   Return none when no `container` element starts after `prolated_offset`::

      abjad> staff = Staff(macros.scale(4))
      abjad> containertools.get_first_element_starting_strictly_after_prolated_offset(staff, 99) is None
      True

   .. versionchanged:: 1.1.2
      renamed ``containertools.get_leftmost_element_starting_after_prolated_offset( )`` to
      ``containertools.get_first_element_starting_strictly_after_prolated_offset( )``.
   '''

   prolated_offset = Fraction(prolated_offset)

   for element in container:
      if prolated_offset < element._offset.start:
         return element
