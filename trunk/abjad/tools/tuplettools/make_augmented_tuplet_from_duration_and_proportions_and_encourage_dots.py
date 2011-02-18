from abjad.tools.tuplettools._make_tuplet_from_duration_with_proportions_and_encourage_dots \
   import _make_tuplet_from_duration_with_proportions_and_encourage_dots


def make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, proportions):
   '''.. versionadded:: 1.1.2

   Make augmented tuplet from `duration` and `proportions` and encourage dots::

      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(Fraction(3, 16), [1, 1, 1, -1, -1])
      {@ 5:8 c'64., c'64., c'64., r64., r64. @}

   Reduce `proportions` relative to each other.

   Interpret negative `proportions` as rests.

   Return fixed-duration tuplet.

   .. versionchanged:: 1.1.2
      renamed ``divide.duration_into_arbitrary_augmentation_dotted( )`` to
      ``tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots( )``.
   '''

   return _make_tuplet_from_duration_with_proportions_and_encourage_dots(
      duration, proportions, 'augmentation')
