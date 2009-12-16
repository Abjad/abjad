from abjad.tools.containertools.get_first_element_starting_not_before_prolated_offset import get_first_element_starting_not_before_prolated_offset


def get_first_index_starting_not_before_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return first ``i`` such that 
   ``container[i].offset.prolated <= prolated_offset``. ::
   
      abjad> staff = Staff(construct.scale(8))
      abjad> containertools.get_first_index_starting_not_before_prolated_offset(staff, Rational(5, 32))
      2

   Otherwise, return none. ::

      abjad> staff = Staff(construct.scale(8))
      abjad> containertools.get_first_index_starting_not_before_prolated_offset(staff, Rational(15, 8)) is None
      True
   '''

   ## get element in container
   element = get_first_element_starting_not_before_prolated_offset(
      container, prolated_offset)

   ## return none if no such element in container
   if element is None:
      return None

   ## get index of element in container
   index = container.index(element)

   ## return index of element in container
   return index
