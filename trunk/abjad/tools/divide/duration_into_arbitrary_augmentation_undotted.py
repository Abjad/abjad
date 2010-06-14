#from abjad.tools.divide._duration_into_arbitrary_fixed_duration_tuplet_undotted import \
#   _duration_into_arbitrary_fixed_duration_tuplet_undotted
from abjad.tools.tuplettools._make_tuplet_from_duration_with_proportions_and_avoid_dots \
   import _make_tuplet_from_duration_with_proportions_and_avoid_dots


def duration_into_arbitrary_augmentation_undotted(duration, proportions):
   '''.. versionadded:: 1.1.2

   Divide `duration` into fixed-duration tuplet
   according to arbitrary integer `proportions`.

   Interpret `proportions` as a ratio. That is, reduce the 
   integers in `proportions` relative to each other.

   Return non-trivial tuplets as augmentations.

   Where ``proportions[i] == 1`` for all ``i <= len(proportions) - 1``, 
   return tupletted notes strictly without dots. ::

      abjad> duration = Rational(3, 16)
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1])
      {@ 2:3 c'8 @}
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 1])
      {@ 2:3 c'16, c'16 @}
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 1, 1])
      {@ 1:1 c'16, c'16, c'16 @}
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 1, 1, 1])
      {@ 2:3 c'32, c'32, c'32, c'32 @}
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 1, 1, 1, 1])
      {@ 5:6 c'32, c'32, c'32, c'32, c'32 @}

   Where ``proportions[i] != 1`` for some ``i <= len(proportions) - 1``, 
   allow tupletted notes to return with dots. ::

      abjad> duration = Rational(3, 16)
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1])
      {@ 2:3 c'8 @}
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 2, 2])
      {@ 5:6 c'32, c'16, c'16 @}
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 2, 2, 3])
      {@ 2:3 c'64, c'32, c'32, c'32. @}
      abjad> print divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 2, 2, 3, 3])
      {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}
   '''

   #return _duration_into_arbitrary_fixed_duration_tuplet_undotted(
   #   duration, proportions, 'augmentation') 
   return _make_tuplet_from_duration_with_proportions_and_avoid_dots(
       duration, proportions, 'augmentation')
