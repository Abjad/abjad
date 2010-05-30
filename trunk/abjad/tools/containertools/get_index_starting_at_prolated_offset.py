from abjad.exceptions import MissingComponentError
from abjad.tools.containertools.get_element_starting_at_prolated_offset \
   import get_element_starting_at_prolated_offset


def get_index_starting_at_prolated_offset(container, prolated_offset):
   '''.. versionadded:: 1.1.2

   Return index of `container` element starting at exactly
   `prolated_offset`::

      abjad> voice = Voice(construct.scale(8))
      abjad> containertools.get_index_starting_at_prolated_offset(voice, Rational(6, 8))
      6
   
   Raise index error when no `container` element starts
   at exactly `prolated_offset`::

      abjad> voice = Voice(construct.scale(8))
      abjad> containertools.get_index_starting_at_prolated_offset(voice, Rational(15, 8))
      IndexError
   '''

   ## find element in container starting at prolated offset
   try:
      element = get_element_starting_at_prolated_offset(
         container, prolated_offset)

   ## raise index error when no container element starts at prolated offset
   except MissingComponentError:
      raise IndexError

   ## find index of element in container
   index = container.index(element)

   ## return index of element in container
   return index
