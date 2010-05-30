from abjad.tools.containertools.get_leftmost_element_starting_not_before_prolated_offset import get_leftmost_element_starting_not_before_prolated_offset


def get_leftmost_index_starting_not_before_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return index of leftmost `container` element 
   starting not before `prolated_offset`::

      abjad> staff = Staff(construct.scale(4))
      abjad> containertools.get_leftmost_index_starting_not_before_prolated_offset(staff, Rational(1, 8))
      1

   Raise index error when no `container` element starts
   not before `prolated_offset`::

      abjad> staff = Staff(construct.scale(4))
      abjad> containertools.get_leftmost_index_starting_not_before_prolated_offset(staff, 99)
      IndexError
   '''

   ## get element in container
   element = get_leftmost_element_starting_not_before_prolated_offset(
      container, prolated_offset)

   ## raise index error if no element in container starts not before offset
   if element is None:
      raise IndexError

   ## get index of element in container
   index = container.index(element)

   ## return index of element in container
   return index
