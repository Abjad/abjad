from abjad.tools import componenttools
from abjad.tools import durationtools


# TODO: move to tuplettools
def leaf_to_tuplet_with_n_notes_of_equal_written_duration(leaf, n, diminution=True):
    '''Change `leaf` to tuplet `n` notes of equal written duration.

    Example 1. Change leaf to augmented tuplet::

        >>> for n in range(1, 11):
        ...     note = Note(0, (3, 16))
        ...     tuplet = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(
        ...         note, n, diminution=False)
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

    Example 2. Change to leaf diminished tuplet::

        >>> for n in range(1, 11):
        ...     note = Note(0, (3, 16))
        ...     tuplet = tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration(
        ...         note, n, diminution=True)
        ...     print tuplet
        ...
        {@ 1:1 c'8. @}
        {@ 1:1 c'16., c'16. @}
        {@ 1:1 c'16, c'16, c'16 @}
        {@ 1:1 c'32., c'32., c'32., c'32. @}
        {@ 5:4 c'32., c'32., c'32., c'32., c'32. @}
        {@ 1:1 c'32, c'32, c'32, c'32, c'32, c'32 @}
        {@ 7:4 c'32., c'32., c'32., c'32., c'32., c'32., c'32. @}
        {@ 1:1 c'64., c'64., c'64., c'64., c'64., c'64., c'64., c'64. @}
        {@ 3:2 c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32 @}
        {@ 5:4 c'64., c'64., c'64., c'64., c'64., c'64., c'64., c'64., c'64., c'64. @}

    Return fixed-duration tuplet.
    '''
    from abjad.tools import notetools
    from abjad.tools import tuplettools

    # find target duration of fixed-duration tuplet
    target_duration = leaf.written_duration

    # find prolated duration of each note in tuplet
    prolated_duration = target_duration / n

    # find written duration of each note in tuplet
    #if prolation == 'diminution':
    if diminution:
        written_duration = durationtools.rational_to_equal_or_greater_assignable_rational(
            prolated_duration)
    #elif prolation == 'augmentation':
    else:
        written_duration = durationtools.rational_to_equal_or_lesser_assignable_rational(
            prolated_duration)

    # make tuplet notes
    notes = notetools.Note(0, written_duration) * n

    # make tuplet
    tuplet = tuplettools.FixedDurationTuplet(target_duration, notes)

    # give leaf position in score structure to tuplet
    componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [tuplet])

    # return tuplet
    return tuplet
