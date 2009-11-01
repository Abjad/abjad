from abjad.tools.divide._leaf_into_even_fixed_duration_tuplet import \
   _leaf_into_even_fixed_duration_tuplet


def leaf_into_even_augmentation(l, divisions):
   '''Divide written duration of `l` into even `divisions`.

   Return (augmented) fixed-duration tuplet. ::

      abjad> for divisions in range(1, 11):
      ...     note = Note(0, (3, 16))
      ...     tuplet = divide.leaf_into_even_augmentation(note, divisions)
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
   '''

   return _leaf_into_even_fixed_duration_tuplet(l, divisions, 'augmentation')
