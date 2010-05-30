from abjad.tools.containertools.get_rightmost_index_starting_before_prolated_offset import get_rightmost_index_starting_before_prolated_offset


def contents_delete_starting_before_prolated_offset(
   container, prolated_offset):
   r'''.. versionadded:: 1.1.2

   Delete `container` contents starting before `prolated_offset`::

      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> containertools.contents_delete_starting_before_prolated_offset(staff, Rational(1, 8))
      Staff{3}

   ::

      abjad> f(staff)
      \new Staff {
         d'8 [
         e'8
         f'8 ]
      }

   Return `container`.
   '''

   ## get index
   try:
      index = get_rightmost_index_starting_before_prolated_offset(
         container, prolated_offset)

   ## return container if no index
   except IndexError:
      return container

   ## delete elements
   del(container[:index+1])

   ## return container
   return container
