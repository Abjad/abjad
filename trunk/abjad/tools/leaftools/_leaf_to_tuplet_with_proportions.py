from abjad.exceptions import AssignabilityError
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import mathtools


def _leaf_to_tuplet_with_proportions(l, divisions, prolation):
    '''Divide written duration of `l` according to `divisions`
    and `prolation`.
    '''
    from abjad.tools.notetools.make_notes import make_notes
    from abjad.tools.notetools.Note import Note
    from abjad.tools import tuplettools

    # find target duration of fixed-duration tuplet
    target_duration = l.written_duration

    # find basic prolated duration of note in tuplet
    basic_prolated_duration = target_duration / sum(divisions)

    # find basic written duration of note in tuplet
    basic_written_duration = durationtools.rational_to_equal_or_greater_assignable_rational(
        basic_prolated_duration)

    # find written duration of each note in tuplet
    written_durations = [x * basic_written_duration for x in divisions]

    # make tuplet notes
    try:
        notes = [Note(0, x) for x in written_durations]
    except AssignabilityError:
        denominator = target_duration._denominator
        note_durations = [durationtools.Duration(x, denominator) for x in divisions]
        notes = make_notes(0, note_durations)

    # make tuplet
    tuplet = tuplettools.FixedDurationTuplet(target_duration, notes)

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

    # give leaf position in score structure to tuplet
    componenttools.move_parentage_and_spanners_from_components_to_components([l], [tuplet])

    # return tuplet
    return tuplet
