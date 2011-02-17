from abjad.tools.tuplettools._make_tuplet_from_duration_with_proportions_and_avoid_dots \
   import _make_tuplet_from_duration_with_proportions_and_avoid_dots


def make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(duration, proportions):
   '''.. versionadded:: 1.1.2

   Make augmented tuplet from `duration` and `proportions` and avoid dots.

   Return tupletted leaves strictly without dots when all `proportions` equal ``1``::
   
      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(Fraction(3, 16), [1, 1, 1, 1, 1])
      {@ 5:6 c'32, c'32, c'32, c'32, c'32 @}

   Allow tupletted leaves to return with dots when some `proportions` do not equal ``1``::

      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(Fraction(3, 16), [1, 2, 2, 3, 3])
      {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}

   Interpret negative `proportions` as rests::

      abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(Fraction(3, 16), [1, -2, -2, 3, 3])
      {@ 11:12 c'64, r32, r32, c'32., c'32. @}

   Reduce `proportions` relative to each other.

   Return fixed-duration tuplet.

   .. versionchanged:: 1.1.2
      renamed ``divide.duration_into_arbitrary_augmentation_undotted( )`` to
      ``tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots( )``.
   '''

   return _make_tuplet_from_duration_with_proportions_and_avoid_dots(
       duration, proportions, 'augmentation')
