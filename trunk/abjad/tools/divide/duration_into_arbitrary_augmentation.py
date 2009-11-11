from abjad.tools.divide._duration_into_arbitrary_fixed_duration_tuplet import \
   _duration_into_arbitrary_fixed_duration_tuplet


def duration_into_arbitrary_augmentation(duration, divisions):
   '''Divide `duration` into arbitrary `divisions`.

   Return (augmented) fixed-duration tuplet. ::

      abjad> duration = Rational(3, 16)
      abjad> print divide.duration_into_arbitrary_augmentation(duration, [1])
      {@ 1:1 c'8. @}
      abjad> print divide.duration_into_arbitrary_augmentation(duration, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print divide.duration_into_arbitrary_augmentation(duration, [1, 2, 2])
      {@ 5:6 c'32, c'16, c'16 @}
      abjad> print divide.duration_into_arbitrary_augmentation(duration, [1, 2, 2, 3])
      {@ 2:3 c'64, c'32, c'32, c'32. @}
      abjad> print divide.duration_into_arbitrary_augmentation(duration, [1, 2, 2, 3, 3])
      {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}
      abjad> print divide.duration_into_arbitrary_augmentation(duration, [1, 2, 2, 3, 3, 4])
      {@ 5:8 c'128, c'64, c'64, c'64., c'64., c'32 @}

   Series of dotted values are allowed. ::

      abjad> divide.duration_into_arbitrary_augmentation(Rational(3, 16), [1, 1, 1, 1, 1])
      FixedDurationTuplet(3/16, [c'64., c'64., c'64., c'64., c'64.])
   '''

   return _duration_into_arbitrary_fixed_duration_tuplet(
      duration, divisions, 'augmentation') 
