from abjad.tools.notetools.Note import Note
from abjad.tools.resttools.Rest import Rest
from abjad.exceptions import AssignabilityError
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet
from abjad.tools.tuplettools.change_augmented_tuplets_in_expr_to_diminished import change_augmented_tuplets_in_expr_to_diminished
from abjad.tools.tuplettools.change_diminished_tuplets_in_expr_to_augmented import change_diminished_tuplets_in_expr_to_augmented
from abjad.tools.tuplettools.fix_contents_of_tuplets_in_expr import fix_contents_of_tuplets_in_expr
from abjad.tools import durationtools


def _make_tuplet_from_duration_with_proportions_and_encourage_dots(
    duration, divisions, prolation, direction = 'big-endian'):

    # reduce divisions relative to each other
    divisions = sequencetools.divide_sequence_elements_by_greatest_common_divisor(divisions)

    # find basic prolated duration of note in tuplet
    #basic_prolated_duration = duration / sum(divisions)
    basic_prolated_duration = duration / mathtools.weight(divisions)

    # TODO: only this call differs from _duration_into_arbitrary_fixed_duration_tuplet_undotted;
    #         so combined the two functions. #
    # find basic written duration of note in tuplet
    basic_written_duration = durationtools.rational_to_equal_or_greater_assignable_rational(
        basic_prolated_duration)

    # find written duration of each note in tuplet
    written_durations = [x * basic_written_duration for x in divisions]

    # make tuplet leaves
    try:
        notes = [Note(0, x) if 0 < x else Rest(abs(x)) for x in written_durations]
    except AssignabilityError:
        denominator = duration._denominator
        note_durations = [durationtools.Duration(x, denominator) for x in divisions]
        pitches = [None if note_duration < 0 else 0 for note_duration in note_durations]
        leaf_durations = [abs(note_duration) for note_duration in note_durations]
        notes = leaftools.make_leaves(pitches, leaf_durations, direction = direction)

    # make tuplet
    tuplet = FixedDurationTuplet(duration, notes)

    # fix tuplet contents if necessary
    fix_contents_of_tuplets_in_expr(tuplet)

    # switch prolation if necessary
    if not tuplet.multiplier == 1:
        if prolation == 'diminution':
            if not tuplet.is_diminution:
                change_augmented_tuplets_in_expr_to_diminished(tuplet)
        else:
            if tuplet.is_diminution:
                change_diminished_tuplets_in_expr_to_augmented(tuplet)

#   # give leaf position in score structure to tuplet
#   containertools.move_parentage_children_and_spanners_from_components_to_empty_container(
#     [l], tuplet)

    # return tuplet
    return tuplet
