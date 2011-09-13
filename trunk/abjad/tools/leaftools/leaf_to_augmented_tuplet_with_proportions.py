from abjad.tools.leaftools._leaf_to_tuplet_with_proportions import _leaf_to_tuplet_with_proportions


def leaf_to_augmented_tuplet_with_proportions(leaf, proportions):
    '''.. versionadded:: 2.0

    Change `leaf` to augmented tuplet with `proportions`::

        abjad> note = Note(0, (3, 16))
        abjad> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1])
        {@ 1:1 c'8. @}
        abjad> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2])
        {@ 1:1 c'16, c'8 @}
        abjad> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2])
        {@ 5:8 c'64., c'32., c'32. @}
        abjad> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3])
        {@ 2:3 c'64, c'32, c'32, c'32. @}
        abjad> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3, 3])
        {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}
        abjad> print leaftools.leaf_to_augmented_tuplet_with_proportions(note, [1, 2, 2, 3, 3, 4])
        {@ 5:8 c'128, c'64, c'64, c'64., c'64., c'32 @}

    Return augmented fixed-duration tuplet.
    '''

    return _leaf_to_tuplet_with_proportions(leaf, proportions, 'augmentation')
