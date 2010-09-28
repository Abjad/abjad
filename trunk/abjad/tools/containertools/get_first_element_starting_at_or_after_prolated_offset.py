from abjad.core import Fraction


def get_first_element_starting_at_or_after_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return leftmost `container` element starting not before `prolated_offset`::

      abjad> staff = Staff(macros.scale(4))
      abjad> containertools.get_first_element_starting_at_or_after_prolated_offset(staff, Fraction(1, 8))
      Note(d', 8)

   Return none when no `container` element starts not before `prolated_offset`::

      abjad> staff = Staff(macros.scale(4))
      abjad> containertools.get_first_element_starting_at_or_after_prolated_offset(staff, 99) is None
      True

   .. versionchanged:: 1.1.2
      renamed ``containertools.get_leftmost_element_starting_not_before_prolated_offset( )`` to
      ``containertools.get_first_element_starting_at_or_after_prolated_offset( )``.
   '''

   prolated_offset = Fraction(prolated_offset)

   for element in container:
      if prolated_offset <= element.offset.start:
         return element
