#from abjad.tools.divide._duration_into_arbitrary_fixed_duration_tuplet_dotted import \
#   _duration_into_arbitrary_fixed_duration_tuplet_dotted
from abjad.tools.tuplettools._make_tuplet_from_duration_with_proportions_and_encourage_dots \
   import _make_tuplet_from_duration_with_proportions_and_encourage_dots


def make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, proportions):
   '''.. versionadded:: 1.1.2

   Divide `duration` into fixed-duration tuplet
   according to arbitrary integer `proportions`.

   Interpret `proportions` as a ratio. That is, reduce the 
   integers in `proportions` relative to each other.

   Return non-trivial tuplets as augmentations.

   Where ``proportions[i] == 1`` for all ``i <= len(proportions) - 1``, 
   allow tupletted notes to carry dots. ::

      abjad> duration = Rational(3, 16)
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1])
      {@ 1:1 c'8. @}
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 1])
      {@ 1:1 c'16., c'16. @}
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 1, 1])
      {@ 1:1 c'16, c'16, c'16 @}
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 1, 1, 1])
      {@ 1:1 c'32., c'32., c'32., c'32. @}
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 1, 1, 1, 1])
      {@ 5:8 c'64., c'64., c'64., c'64., c'64. @}

   Where ``proportions[i] != 1`` for some ``i <= len(proportions) - 1``, 
   allow tupletted notes to carry dots. ::

      abjad> duration = Rational(3, 16)
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1])
      {@ 1:1 c'8. @}
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 2, 2])
      {@ 5:8 c'64., c'32., c'32. @}
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 2, 2, 3])
      {@ 2:3 c'64, c'32, c'32, c'32. @}
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 2, 2, 3, 3])
      {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}

   .. versionchanged:: 1.1.2
      renamed ``divide.duration_into_arbitrary_augmentation_dotted( )`` to
      ``tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots( )``.
   '''

   #return _duration_into_arbitrary_fixed_duration_tuplet_dotted(
   #   duration, proportions, 'augmentation') 
   return _make_tuplet_from_duration_with_proportions_and_encourage_dots(
      duration, proportions, 'augmentation')
