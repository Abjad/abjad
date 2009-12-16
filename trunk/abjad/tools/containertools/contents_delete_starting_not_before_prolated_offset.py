from abjad.tools.containertools.get_first_index_starting_not_before_prolated_offset import get_first_index_starting_not_before_prolated_offset


def contents_delete_starting_not_before_prolated_offset(
   container, prolated_offset):
   r'''.. versionadded:: 1.1.2

   Delete ``container[i:]`` such that none of the eleements in 
   ``container[i:]`` start before `prolated_offset`. ::

      abjad> staff = Staff(construct.scale(8))
      abjad> containertools.contents_delete_from_prolated_offset_forward(staff, Rational(3, 8))
      Staff{2}
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
      }
   '''

   ## get index
   index = get_first_index_starting_not_before_prolated_offset(
      container, prolated_offset)

   ## delete elements latter part of container
   del(container[index:])

   ## return trimmed container
   return container
