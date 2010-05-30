from abjad.tools.containertools.get_leftmost_index_starting_after_prolated_offset import get_leftmost_index_starting_after_prolated_offset


def contents_delete_starting_after_prolated_offset(
   container, prolated_offset):
   r'''.. versionadded:: 1.1.2

   Delete `container` contents starting after `prolated_offset`::

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
      
      abjad> containertools.contents_delete_starting_after_prolated_offset(staff, Rational(1, 8))
      Staff{2}
      
   ::
      
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ]
      }

   Return `container`.
   '''

   ## get index
   try:
      index = get_leftmost_index_starting_after_prolated_offset(
         container, prolated_offset)

   ## return container if no index
   except IndexError:
      return container

   ## delete elements
   del(container[index:])

   ## return container
   return container
