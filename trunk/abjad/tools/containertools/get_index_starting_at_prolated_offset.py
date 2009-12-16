from abjad.tools.containertools.get_element_starting_at_prolated_offset \
   import get_element_starting_at_prolated_offset


def get_index_starting_at_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return index of first element in `container` starting at exactly
   `prolated_offset`. ::

      abjad> voice = Voice(construct.scale(8))
      abjad> containertools.get_index_start_at_prolated_offset(voice, Rational(6, 8))
      6
   
   Raise missing component error when no element in `container` starts
   at exactly `prolated_offset`. ::

      abjad> voice = Voice(construct.scale(8))
      abjad> containertools.get_index_start_at_prolated_offset(voice, Rational(15, 8))
      MissingComponentError
   '''

   ## find element in container starting at prolated offset
   element = get_element_starting_at_prolated_offset(container, prolated_offset)

   ## find index of element in container
   index = container.index(element)

   ## return index of element in container
   return index
