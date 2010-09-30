from abjad.core import Fraction


def get_first_element_starting_before_or_at_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return rightmost element in `container` starting not after `prolated_offset`::
   
      abjad> staff = Staff(macros.scale(4))
      abjad> containertools.get_first_element_starting_before_or_at_prolated_offset(staff, Fraction(1, 8))
      Note(d', 8)

   Return none when no element in `container` starts not after `prolated_offset`::

      abjad> staff = Staff(macros.scale(4))
      abjad> containertools.get_first_element_starting_before_or_at_prolated_offset(staff, Fraction(-1, 8)) is None
      True

   .. versionchanged:: 1.1.2
      renamed ``containertools.get_rightmost_element_starting_not_after_prolated_offset( )`` to
      ``containertools.get_first_element_starting_before_or_at_prolated_offset( )``.
   '''

   prolated_offset = Fraction(prolated_offset)

   for element in reversed(container):
      if element._offset.start <= prolated_offset:
         return element
