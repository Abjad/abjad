from abjad.rational import Rational


def get_leftmost_element_starting_not_before_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return leftmost `container` element starting not before `prolated_offset`::

      abjad> staff = Staff(construct.scale(4))
      abjad> containertools.get_leftmost_element_starting_not_before_prolated_offset(staff, Rational(1, 8))
      Note(d', 8)

   Return none when no `container` element starts not before `prolated_offset`::

      abjad> staff = Staff(construct.scale(4))
      abjad> containertools.get_leftmost_element_starting_not_before_prolated_offset(staff, 99) is None
      True
   '''

   prolated_offset = Rational(prolated_offset)

   for element in container:
      if prolated_offset <= element.offset.prolated.start:
         return element
