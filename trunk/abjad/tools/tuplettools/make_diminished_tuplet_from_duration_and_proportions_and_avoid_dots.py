from abjad.tools.tuplettools._make_tuplet_from_duration_with_proportions_and_avoid_dots import _make_tuplet_from_duration_with_proportions_and_avoid_dots

def make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(
    duration, proportions, direction = 'big-endian'):
    r'''.. versionadded:: 2.0

    Make diminished tuplet from `duration` and nonzero integer `proportions`.

    Return tupletted leaves strictly without dots when all `proportions` equal ``1``::

        abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(
        ... Fraction(3, 16), [1, 1, 1, -1, -1])
        {@ 5:3 c'16, c'16, c'16, r16, r16 @}

    Allow tupletted leaves to return with dots when some `proportions` do not equal ``1``::

        abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(
        ... Fraction(3, 16), [1, -2, -2, 3, 3])
        {@ 11:6 c'32, r16, r16, c'16., c'16. @}

    Interpret nonassignable `proportions` according to `direction`::

        abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(
        ... Fraction(3, 16), [5, -1, 5], direction = 'little-endian')
        {@ 11:6 c'32, c'8, r32, c'32, c'8 @}

    Reduce `proportions` relative to each other.

    Interpret negative `proportions` as rets.

    Return fixed-duration tuplet.

    .. versionchanged:: 2.0
        renamed ``divide.duration_into_arbitrary_diminution_undotted()`` to
        ``tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots()``.
    '''

    return _make_tuplet_from_duration_with_proportions_and_avoid_dots(
        duration, proportions, 'diminution', direction = direction)
