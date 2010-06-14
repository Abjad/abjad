#from abjad.tools.divide._leaf_into_even_fixed_duration_tuplet import \
#   _leaf_into_even_fixed_duration_tuplet
from abjad.tools.leaftools._leaf_to_tuplet_with_n_notes_of_equal_written_duration import \
   _leaf_to_tuplet_with_n_notes_of_equal_written_duration


def leaf_into_even_diminution(leaf, n):
   '''Divide written duration of `leaf` into even `n`.

   Return (diminshed) fixed-duration tuplet. ::

      abjad> for n in range(1, 11):
      ...     note = Note(0, (3, 16))
      ...     tuplet = divide.leaf_into_even_diminution(note, n)
      ...     print tuplet
      ... 
      {@ 1:1 c'8. @}
      {@ 1:1 c'16., c'16. @}
      {@ 1:1 c'16, c'16, c'16 @}
      {@ 1:1 c'32., c'32., c'32., c'32. @}
      {@ 5:3 c'16, c'16, c'16, c'16, c'16 @}
      {@ 1:1 c'32, c'32, c'32, c'32, c'32, c'32 @}
      {@ 7:6 c'32, c'32, c'32, c'32, c'32, c'32, c'32 @}
      {@ 1:1 c'64., c'64., c'64., c'64., c'64., c'64., c'64., c'64. @}
      {@ 3:2 c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32 @}
      {@ 5:3 c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32 @}
   '''

   #return _leaf_into_even_fixed_duration_tuplet(leaf, n, 'diminution')
   return _leaf_to_tuplet_with_n_notes_of_equal_written_duration(leaf, n, 'diminution')
