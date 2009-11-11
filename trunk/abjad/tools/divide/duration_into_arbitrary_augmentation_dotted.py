from abjad.tools.divide._duration_into_arbitrary_fixed_duration_tuplet_dotted import \
   _duration_into_arbitrary_fixed_duration_tuplet_dotted


def duration_into_arbitrary_augmentation_dotted(duration, divisions):
   '''.. versionadded:: 1.1.2

   Divide `duration` into fixed-duration tuplet
   according to arbitrary integer `divisions`.

   Interpret `divisions` as a ratio. That is, reduce the 
   integers in `divisions` relative to each other.

   Return non-trivial tuplets as augmentations.

   Where ``divisions[i] == 1`` for all ``i <= len(divisions) - 1``, 
   allow tupletted notes to carry dots. ::

      abjad> duration = Rational(3, 16)
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1])
      {@ 1:1 c'8. @}
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1, 1])
      {@ 1:1 c'16., c'16. @}
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1, 1, 1])
      {@ 1:1 c'16, c'16, c'16 @}
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1, 1, 1, 1])
      {@ 1:1 c'32., c'32., c'32., c'32. @}
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1, 1, 1, 1, 1])
      {@ 5:8 c'64., c'64., c'64., c'64., c'64. @}

   Where ``divisions[i] != 1`` for some ``i <= len(divisions) - 1``, 
   allow tupletted notes to carry dots. ::

      abjad> duration = Rational(3, 16)
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1])
      {@ 1:1 c'8. @}
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1, 2, 2])
      {@ 5:8 c'64., c'32., c'32. @}
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1, 2, 2, 3])
      {@ 2:3 c'64, c'32, c'32, c'32. @}
      abjad> print divide.duration_into_arbitrary_augmentation_dotted(duration, [1, 2, 2, 3, 3])
      {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}
   '''

   return _duration_into_arbitrary_fixed_duration_tuplet_dotted(
      duration, divisions, 'augmentation') 
