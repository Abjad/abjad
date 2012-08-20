def leaf_to_augmented_tuplet_with_proportions(leaf, proportions):
    '''.. versionadded:: 2.0

    Change `leaf` to augmented tuplet with `proportions`::

        >>> note = Note(0, (3, 16))
        >>> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1])
        {@ 1:1 c'8. @}
        >>> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2])
        {@ 1:1 c'16, c'8 @}
        >>> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2])
        {@ 5:8 c'64., c'32., c'32. @}
        >>> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3])
        {@ 2:3 c'64, c'32, c'32, c'32. @}
        >>> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3, 3])
        {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}
        >>> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3, 3, 4])
        {@ 5:8 c'128, c'64, c'64, c'64., c'64., c'32 @}

    Return augmented fixed-duration tuplet.
    '''
    from abjad.tools import leaftools

    return leaftools.leaf_to_tuplet_with_proportions(leaf, proportions, diminution=False)
