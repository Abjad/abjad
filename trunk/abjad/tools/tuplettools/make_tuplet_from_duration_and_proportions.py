from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools import sequencetools


def make_tuplet_from_duration_and_proportions(duration, divisions, prolation, avoid_dots=True, big_endian=True):
    from abjad.tools import tuplettools

    # reduce divisions relative to each other
    divisions = sequencetools.divide_sequence_elements_by_greatest_common_divisor(divisions)

    # find basic prolated duration of note in tuplet
    #basic_prolated_duration = duration / sum(divisions)
    basic_prolated_duration = duration / mathtools.weight(divisions)

    # find basic written duration of note in tuplet
    if avoid_dots:
        basic_written_duration = durationtools.rational_to_equal_or_greater_binary_rational(
            basic_prolated_duration)
    else:
        basic_written_duration = durationtools.rational_to_equal_or_greater_assignable_rational(
            basic_prolated_duration)

    # find written duration of each note in tuplet
    written_durations = [x * basic_written_duration for x in divisions]

    # make tuplet leaves
    try:
        notes = [notetools.Note(0, x) if 0 < x else resttools.Rest(abs(x)) for x in written_durations]
    except AssignabilityError:
        denominator = duration._denominator
        note_durations = [durationtools.Duration(x, denominator) for x in divisions]
        pitches = [None if note_duration < 0 else 0 for note_duration in note_durations]
        leaf_durations = [abs(note_duration) for note_duration in note_durations]
        notes = leaftools.make_leaves(pitches, leaf_durations, big_endian=big_endian)

    # make tuplet
    tuplet = tuplettools.FixedDurationTuplet(duration, notes)

    # fix tuplet contents if necessary
    tuplettools.fix_contents_of_tuplets_in_expr(tuplet)

    # switch prolation if necessary
    if not tuplet.multiplier == 1:
        if prolation == 'diminution':
            if not tuplet.is_diminution:
                tuplettools.change_augmented_tuplets_in_expr_to_diminished(tuplet)
        else:
            if tuplet.is_diminution:
                tuplettools.change_diminished_tuplets_in_expr_to_augmented(tuplet)

    # return tuplet
    return tuplet
