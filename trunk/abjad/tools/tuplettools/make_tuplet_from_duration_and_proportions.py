from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools import sequencetools


def make_tuplet_from_duration_and_proportions(duration, proportions, 
    avoid_dots=True, big_endian=True, is_diminution=True):
    r'''.. versionadded:: 2.10

    Make tuplet from `duration` and `proportions`.

    Example set 1. Make augmented tuplet from `duration` and `proportions` and avoid dots.

    Return tupletted leaves strictly without dots when all `proportions` equal ``1``::

        >>> print tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [1, 1, 1, -1, -1], avoid_dots=True, is_diminution=False)
        {@ 5:6 c'32, c'32, c'32, r32, r32 @}

    Allow tupletted leaves to return with dots when some `proportions` do not equal ``1``::

        >>> print tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [1, -2, -2, 3, 3], avoid_dots=True, is_diminution=False)
        {@ 11:12 c'64, r32, r32, c'32., c'32. @}

    Interpret nonassignable `proportions` according to `big_endian`::

        >>> print tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [5, -1, 5], avoid_dots=True, big_endian=False, is_diminution=False)
        {@ 11:12 c'64, c'16, r64, c'64, c'16 @}

    Example set 2. Make augmented tuplet from `duration` and `proportions` and encourage dots::

        >>> tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [1, 1, 1, -1, -1], avoid_dots=False, is_diminution=False)
        FixedDurationTuplet(3/16, [c'64., c'64., c'64., r64., r64.])

    Interpret nonassignable `proportions` according to `big_endian`::

        >>> tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [5, -1, 5], avoid_dots=False, big_endian=False, is_diminution=False)
        FixedDurationTuplet(3/16, [c'32..., r128., c'32...])

    Example set 3. Make diminished tuplet from `duration` and nonzero integer `proportions`.

    Return tupletted leaves strictly without dots when all `proportions` equal ``1``::

        >>> print tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [1, 1, 1, -1, -1], avoid_dots=True, is_diminution=True)
        {@ 5:3 c'16, c'16, c'16, r16, r16 @}

    Allow tupletted leaves to return with dots when some `proportions` do not equal ``1``::

        >>> print tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [1, -2, -2, 3, 3], avoid_dots=True, is_diminution=True)
        {@ 11:6 c'32, r16, r16, c'16., c'16. @}

    Interpret nonassignable `proportions` according to `big_endian`::

        >>> print tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [5, -1, 5], avoid_dots=True, big_endian=False, is_diminution=True)
        {@ 11:6 c'32, c'8, r32, c'32, c'8 @}

    Example set 4. Make diminished tuplet from `duration` and `proportions` and encourage dots::

        >>> tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [1, 1, 1, -1, -1], avoid_dots=False, is_diminution=True)
        FixedDurationTuplet(3/16, [c'32., c'32., c'32., r32., r32.])

    Interpret nonassignable `proportions` according to `direction`::

        >>> tuplettools.make_tuplet_from_duration_and_proportions(
        ... Fraction(3, 16), [5, -1, 5], avoid_dots=False, big_endian=False, is_diminution=True)
        FixedDurationTuplet(3/16, [c'16..., r64., c'16...])

    Reduce `proportions` relative to each other.

    Interpret negative `proportions` as rests.

    Return fixed-duration tuplet.
    '''
    from abjad.tools import tuplettools

    # reduce proportions relative to each other
    proportions = sequencetools.divide_sequence_elements_by_greatest_common_divisor(proportions)

    # find basic prolated duration of note in tuplet
    basic_prolated_duration = duration / mathtools.weight(proportions)

    # find basic written duration of note in tuplet
    if avoid_dots:
        basic_written_duration = durationtools.rational_to_equal_or_greater_binary_rational(
            basic_prolated_duration)
    else:
        basic_written_duration = durationtools.rational_to_equal_or_greater_assignable_rational(
            basic_prolated_duration)

    # find written duration of each note in tuplet
    written_durations = [x * basic_written_duration for x in proportions]

    # make tuplet leaves
    try:
        notes = [notetools.Note(0, x) if 0 < x else resttools.Rest(abs(x)) for x in written_durations]
    except AssignabilityError:
        denominator = duration._denominator
        note_durations = [durationtools.Duration(x, denominator) for x in proportions]
        pitches = [None if note_duration < 0 else 0 for note_duration in note_durations]
        leaf_durations = [abs(note_duration) for note_duration in note_durations]
        notes = leaftools.make_leaves(pitches, leaf_durations, big_endian=big_endian)

    # make tuplet
    tuplet = tuplettools.FixedDurationTuplet(duration, notes)

    # fix tuplet contents if necessary
    tuplettools.fix_contents_of_tuplets_in_expr(tuplet)

    # switch prolation if necessary
    if not tuplet.multiplier == 1:
        #if prolation == 'diminution':
        if is_diminution:
            if not tuplet.is_diminution:
                tuplettools.change_augmented_tuplets_in_expr_to_diminished(tuplet)
        else:
            if tuplet.is_diminution:
                tuplettools.change_diminished_tuplets_in_expr_to_augmented(tuplet)

    # return tuplet
    return tuplet
