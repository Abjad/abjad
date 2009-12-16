def get_first_element_starting_not_before_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return first ``container[i]`` such that 
   ``container[i].offset.prolated <= prolated_offset``. ::
   
      abjad> staff = Staff(construct.scale(8))
      abjad> containertools.get_first_element_starting_not_before_prolated_offset(staff, Rational(5, 32))
      ??

   Otherwise, return none. ::

      abjad> staff = Staff(construct.scale(8))
      abjad> containertools.get_first_element_starting_not_before_prolated_offset(staff, Rational(15, 8)) is None
      True
   '''

   for element in container:
      if not element.offset.prolated.start <= prolated_offset:
         return element
