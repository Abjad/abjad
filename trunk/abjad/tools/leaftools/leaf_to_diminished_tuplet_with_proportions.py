def leaf_to_diminished_tuplet_with_proportions(leaf, proportions):
    '''.. versionadded:: 2.0

    Change `leaf` to diminished tuplet with `proportions`::

        >>> note = Note(0, (3, 16))
        >>> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1])
        {@ 1:1 c'8. @}
        >>> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2])
        {@ 1:1 c'16, c'8 @}
        >>> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2, 2])
        {@ 5:4 c'32., c'16., c'16. @}
        >>> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2, 2, 3])
        {@ 4:3 c'32, c'16, c'16, c'16. @}
        >>> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2, 2, 3, 3])
        {@ 11:6 c'32, c'16, c'16, c'16., c'16. @}
        >>> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2, 2, 3, 3, 4])
        {@ 5:4 c'64, c'32, c'32, c'32., c'32., c'16 @}

    Return diminshed fixed-duration tuplet.
    '''
    from abjad.tools import leaftools

    return leaftools.leaf_to_tuplet_with_proportions(leaf, proportions, diminution=True)
