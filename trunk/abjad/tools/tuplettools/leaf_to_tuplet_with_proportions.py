from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import mathtools


# TODO: move to tuplettools
def leaf_to_tuplet_with_proportions(leaf, proportions, diminution=True):
    '''Change `leaf` to tuplet with `proportions`.

    Example 1. Change `leaf` to augmented tuplet with `proportions`::

        >>> note = Note(0, (3, 16))

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1], diminution=False)
        {@ 1:1 c'8. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2], diminution=False)
        {@ 1:1 c'16, c'8 @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2, 2], diminution=False)
        {@ 5:8 c'64., c'32., c'32. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2, 2, 3], diminution=False)
        {@ 2:3 c'64, c'32, c'32, c'32. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2, 2, 3, 3], diminution=False)
        {@ 11:12 c'64, c'32, c'32, c'32., c'32. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2, 2, 3, 3, 4], diminution=False)
        {@ 5:8 c'128, c'64, c'64, c'64., c'64., c'32 @}

    Example 2. Change `leaf` to diminished tuplet::

        >>> note = Note(0, (3, 16))

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1], diminution=True)
        {@ 1:1 c'8. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2], diminution=True)
        {@ 1:1 c'16, c'8 @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2, 2], diminution=True)
        {@ 5:4 c'32., c'16., c'16. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2, 2, 3], diminution=True)
        {@ 4:3 c'32, c'16, c'16, c'16. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2, 2, 3, 3], diminution=True)
        {@ 11:6 c'32, c'16, c'16, c'16., c'16. @}

    ::

        >>> print tuplettools.leaf_to_tuplet_with_proportions(
        ...     note, [1, 2, 2, 3, 3, 4], diminution=True)
        {@ 5:4 c'64, c'32, c'32, c'32., c'32., c'16 @}

    Return fixed-duration tuplet.
    '''
    from abjad.tools import notetools
    from abjad.tools import tuplettools

    # find target duration of fixed-duration tuplet
    target_duration = leaf.written_duration

    # find basic prolated duration of note in tuplet
    basic_prolated_duration = target_duration / sum(proportions)

    # find basic written duration of note in tuplet
    basic_written_duration = durationtools.rational_to_equal_or_greater_assignable_rational(
        basic_prolated_duration)

    # find written duration of each note in tuplet
    written_durations = [x * basic_written_duration for x in proportions]

    # make tuplet notes
    try:
        notes = [notetools.Note(0, x) for x in written_durations]
    except AssignabilityError:
        denominator = target_duration._denominator
        note_durations = [durationtools.Duration(x, denominator) for x in proportions]
        notes = notetools.make_notes(0, note_durations)

    # make tuplet
    tuplet = tuplettools.FixedDurationTuplet(target_duration, notes)

    # fix tuplet contents if necessary
    tuplettools.fix_contents_of_tuplets_in_expr(tuplet)

    # switch prolation if necessary
    if not tuplet.multiplier == 1:
        #if prolation == 'diminution':
        if diminution:
            if not tuplet.is_diminution:
                tuplettools.change_augmented_tuplets_in_expr_to_diminished(tuplet)
        else:
            if tuplet.is_diminution:
                tuplettools.change_diminished_tuplets_in_expr_to_augmented(tuplet)

    # give leaf position in score structure to tuplet
    componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [tuplet])

    # return tuplet
    return tuplet
