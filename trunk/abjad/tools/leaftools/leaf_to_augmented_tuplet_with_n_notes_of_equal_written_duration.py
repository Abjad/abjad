#from abjad.tools.divide._leaf_into_even_fixed_duration_tuplet import \
#   _leaf_into_even_fixed_duration_tuplet
from abjad.tools.leaftools._leaf_to_tuplet_with_n_notes_of_equal_written_duration import \
   _leaf_to_tuplet_with_n_notes_of_equal_written_duration


def leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration(leaf, n):
   '''Divide written duration of `leaf` into even `n`.

   Return (augmented) fixed-duration tuplet. ::

      abjad> for n in range(1, 11):
      ...     note = Note(0, (3, 16))
      ...     tuplet = leaftools.leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration(note, n)
      ...     print tuplet
      ... 
      {@ 1:1 c'8. @}
      {@ 1:1 c'16., c'16. @}
      {@ 1:1 c'16, c'16, c'16 @}
      {@ 1:1 c'32., c'32., c'32., c'32. @}
      {@ 5:6 c'32, c'32, c'32, c'32, c'32 @}
      {@ 1:1 c'32, c'32, c'32, c'32, c'32, c'32 @}
      {@ 7:12 c'64, c'64, c'64, c'64, c'64, c'64, c'64 @}
      {@ 1:1 c'64., c'64., c'64., c'64., c'64., c'64., c'64., c'64. @}
      {@ 3:4 c'64, c'64, c'64, c'64, c'64, c'64, c'64, c'64, c'64 @}
      {@ 5:6 c'64, c'64, c'64, c'64, c'64, c'64, c'64, c'64, c'64, c'64 @}

   .. versionchanged:: 1.1.2
      renamed ``divide.leaf_into_even_augmentation( )`` to
      ``leaftools.leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration( )``.
   '''

   #return _leaf_into_even_fixed_duration_tuplet(leaf, n, 'augmentation')
   return _leaf_to_tuplet_with_n_notes_of_equal_written_duration(leaf, n, 'augmentation')
