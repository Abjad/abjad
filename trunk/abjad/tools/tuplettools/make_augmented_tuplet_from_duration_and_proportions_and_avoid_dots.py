from abjad.tools.tuplettools._make_tuplet_from_duration_with_proportions_and_avoid_dots import _make_tuplet_from_duration_with_proportions_and_avoid_dots


def make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
    duration, proportions, direction = 'big-endian'):
    '''.. versionadded:: 2.0

    Make augmented tuplet from `duration` and `proportions` and avoid dots.

    Return tupletted leaves strictly without dots when all `proportions` equal ``1``::

        abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        ... Fraction(3, 16), [1, 1, 1, -1, -1])
        {@ 5:6 c'32, c'32, c'32, r32, r32 @}

    Allow tupletted leaves to return with dots when some `proportions` do not equal ``1``::

        abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        ... Fraction(3, 16), [1, -2, -2, 3, 3])
        {@ 11:12 c'64, r32, r32, c'32., c'32. @}

    Interpret nonassignable `proportions` according to `direction`::

        abjad> print tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots(
        ... Fraction(3, 16), [5, -1, 5], direction = 'little-endian')
        {@ 11:12 c'64, c'16, r64, c'64, c'16 @}

    Reduce `proportions` relative to each other.

    Interpret negative `proportions` as rests.

    Return fixed-duration tuplet.

    .. versionchanged:: 2.0
        renamed ``divide.duration_into_arbitrary_augmentation_undotted()`` to
        ``tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots()``.
    '''

    return _make_tuplet_from_duration_with_proportions_and_avoid_dots(
        duration, proportions, 'augmentation', direction = direction)
