from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools


def leaf_to_tuplet_with_ratio(leaf, proportions, is_diminution=True):
    '''Change `leaf` to tuplet with `proportions`.

    Example 1. Change `leaf` to augmented tuplet with `proportions`:

    ::

        >>> note = Note(0, (3, 16))

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1], is_diminution=False)
        {@ 1:1 c'8. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2], is_diminution=False)
        {@ 1:1 c'16, c'8 @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2, 2], is_diminution=False)
        {@ 5:8 c'64., c'32., c'32. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2, 2, 3], is_diminution=False)
        {@ 2:3 c'64, c'32, c'32, c'32. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2, 2, 3, 3], is_diminution=False)
        {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2, 2, 3, 3, 4], is_diminution=False)
        {@ 5:8 c'128, c'64, c'64, c'64., c'64., c'32 @}

    Example 2. Change `leaf` to diminished tuplet:

    ::

        >>> note = Note(0, (3, 16))

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1], is_diminution=True)
        {@ 1:1 c'8. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2], is_diminution=True)
        {@ 1:1 c'16, c'8 @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2, 2], is_diminution=True)
        {@ 5:4 c'32., c'16., c'16. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2, 2, 3], is_diminution=True)
        {@ 4:3 c'32, c'16, c'16, c'16. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2, 2, 3, 3], is_diminution=True)
        {@ 11:6 c'32, c'16, c'16, c'16., c'16. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_ratio(
        ...     note, [1, 2, 2, 3, 3, 4], is_diminution=True)
        {@ 5:4 c'64, c'32, c'32, c'32., c'32., c'16 @}

    Return fixed-duration tuplet.
    '''
    return leaf._to_tuplet_with_ratio(proportions, is_diminution=is_diminution)
