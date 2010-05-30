from abjad.tools.containertools.get_rightmost_element_starting_not_after_prolated_offset import get_rightmost_element_starting_not_after_prolated_offset


def get_rightmost_index_starting_not_after_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return index of rightmost element in `container`
   starting not after `prolated_offset`::

      abjad> staff = Staff(construct.scale(4))
      abjad> containertools.get_rightmost_index_starting_not_after_prolated_offset(staff, Rational(1, 8))
      1

   Raise index error when no element in `container` starts
   not_after `prolated_offset`::

      abjad> staff = Staff(construct.scale(4))
      abjad> containertools.get_rightmost_index_starting_not_after_prolated_offset(staff, 0)
      IndexError
   '''

   ## get element in container
   element = get_rightmost_element_starting_not_after_prolated_offset(
      container, prolated_offset)

   ## raise index error if not element in container starts not_after offset
   if element is None:
      raise IndexError

   ## get index of element in container
   index = container.index(element)

   ## return index of element in container
   return index
