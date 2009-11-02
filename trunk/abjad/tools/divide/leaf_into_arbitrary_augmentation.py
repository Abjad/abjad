from abjad.tools.divide._leaf_into_arbitrary_fixed_duration_tuplet import \
   _leaf_into_arbitrary_fixed_duration_tuplet


def leaf_into_arbitrary_augmentation(l, divisions):
   '''Divide written duration of `l` into arbitrary `divisions`.

   Return (augmented) fixed-duration tuplet. ::

      abjad> note = Note(0, (3, 16))
      abjad> print divide.leaf_into_arbitrary_augmentation(note, [1])
      {@ 1:1 c'8. @}
      abjad> print divide.leaf_into_arbitrary_augmentation(note, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print divide.leaf_into_arbitrary_augmentation(note, [1, 2, 2])
      {@ 5:6 c'32, c'16, c'16 @}
      abjad> print divide.leaf_into_arbitrary_augmentation(note, [1, 2, 2, 3])
      {@ 2:3 c'64, c'32, c'32, c'32. @}
      abjad> print divide.leaf_into_arbitrary_augmentation(note, [1, 2, 2, 3, 3])
      {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}
      abjad> print divide.leaf_into_arbitrary_augmentation(note, [1, 2, 2, 3, 3, 4])
      {@ 5:8 c'128, c'64, c'64, c'64., c'64., c'32 @}
   '''

   return _leaf_into_arbitrary_fixed_duration_tuplet(
      l, divisions, 'augmentation') 
