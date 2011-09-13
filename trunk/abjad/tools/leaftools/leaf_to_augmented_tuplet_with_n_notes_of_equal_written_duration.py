from abjad.tools.leaftools._leaf_to_tuplet_with_n_notes_of_equal_written_duration import _leaf_to_tuplet_with_n_notes_of_equal_written_duration


def leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration(leaf, n):
    '''.. versionadded:: 2.0

    Change `leaf` to augmented tuplet with `n` notes of equal written duration::

        abjad> for n in range(1, 11):
        ...     note = Note(0, (3, 16))
        ...     tuplet = leaftools.leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration(note, n)
        ...     print tuplet
        ...
        {@ 1:1 c'8. @}
        {@ 1:1 c'16., c'16. @}
        {@ 1:1 c'16, c'16, c'16 @}
        {@ 1:1 c'32., c'32., c'32., c'32. @}
        {@ 5:8 c'64., c'64., c'64., c'64., c'64. @}
        {@ 1:1 c'32, c'32, c'32, c'32, c'32, c'32 @}
        {@ 7:8 c'64., c'64., c'64., c'64., c'64., c'64., c'64. @}
        {@ 1:1 c'64., c'64., c'64., c'64., c'64., c'64., c'64., c'64. @}
        {@ 3:4 c'64, c'64, c'64, c'64, c'64, c'64, c'64, c'64, c'64 @}
        {@ 5:8 c'128., c'128., c'128., c'128., c'128., c'128., c'128., c'128., c'128., c'128. @}

    Return augmented fixed-duration tuplet.
    '''

    return _leaf_to_tuplet_with_n_notes_of_equal_written_duration(leaf, n, 'augmentation')
