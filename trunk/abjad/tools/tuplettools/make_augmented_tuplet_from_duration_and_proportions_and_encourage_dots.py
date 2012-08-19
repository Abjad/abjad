def make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(
    duration, proportions, big_endian=True):
    '''.. versionadded:: 2.0

    Make augmented tuplet from `duration` and `proportions` and encourage dots::

        >>> tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(
        ... Fraction(3, 16), [1, 1, 1, -1, -1])
        FixedDurationTuplet(3/16, [c'64., c'64., c'64., r64., r64.])

    Interpret nonassignable `proportions` according to `direction`::

        >>> tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(
        ... Fraction(3, 16), [5, -1, 5], big_endian=False)
        FixedDurationTuplet(3/16, [c'32..., r128., c'32...])

    Reduce `proportions` relative to each other.

    Interpret negative `proportions` as rests.

    Return fixed-duration tuplet.

    .. versionchanged:: 2.0
        renamed ``divide.duration_into_arbitrary_augmentation_dotted()`` to
        ``tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots()``.
    '''
    from abjad.tools.tuplettools._make_tuplet_from_duration_with_proportions_and_encourage_dots import \
        _make_tuplet_from_duration_with_proportions_and_encourage_dots

    return _make_tuplet_from_duration_with_proportions_and_encourage_dots(
        duration, proportions, 'augmentation', big_endian=big_endian)
