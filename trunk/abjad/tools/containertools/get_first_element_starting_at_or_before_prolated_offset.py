from abjad.rational import Rational


def get_rightmost_element_starting_not_after_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return rightmost element in `container` starting not after `prolated_offset`::
   
      abjad> staff = Staff(construct.scale(4))
      abjad> containertools.get_rightmost_element_starting_not_after_prolated_offset(staff, Rational(1, 8))
      Note(d', 8)

   Return none when no element in `container` starts not after `prolated_offset`::

      abjad> staff = Staff(construct.scale(4))
      abjad> containertools.get_rightmost_element_starting_not_after_prolated_offset(staff, Rational(-1, 8)) is None
      True
   '''

   prolated_offset = Rational(prolated_offset)

   for element in reversed(container):
      if element.offset.prolated.start <= prolated_offset:
         return element
